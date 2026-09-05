from pathlib import Path

CASE52 = Path("cases/52-nand-flash-read-disturb-access-induced-decay.md")
EVID52 = Path("evidence/52-cai-2009-2015-nand-read-disturb-grounding.md")
CASE97 = Path("cases/97-nand-flash-read-disturb-access-conditioned-retention.md")
EVID97 = Path("evidence/97-nand-2002-2015-read-disturb-grounding.md")
README = Path("README.md")
ROADMAP = Path("ROADMAP.md")
INDEX = Path("CASE_INDEX.md")

# --- Canonical Case 52 -----------------------------------------------------
s = CASE52.read_text()
status_start = s.find("**`grounded`** —")
if status_start < 0:
    raise SystemExit("Case52 status start missing")
status_end = s.find("\n\n", status_start)
if status_end < 0:
    raise SystemExit("Case52 status end missing")
new_status = """**`grounded`** — bounded to NAND read disturb from a Fujitsu 2002-priority manufacturer filing through Yu Cai et al.'s 2015 DSN experimental characterization. NASA/JPL's March 2008 qualification study is retained as an independent institutional witness, including its explicit negative result; a 2009-priority Texas Memory Systems patent and a 2013 APSys paper constrain controller/FTL prior-art claims. The case separates measured device behavior, engineering reconstruction, and proposed mitigation/recovery, and does not claim commercial deployment of the 2015 mechanisms."""
if "Fujitsu 2002-priority manufacturer filing" not in s[:status_end]:
    s = s[:status_start] + new_status + s[status_end:]

historical = """### Earlier manufacturer-primary witness — Fujitsu, 2002 priority / 2003 publication

Fujitsu's **US20030137873A1, “Read disturb alleviated flash memory,”** has a 22 January 2002 priority date and a 24 July 2003 U.S. publication date. The original assignee is Fujitsu Ltd. The application explicitly concerns NAND-type Flash and uses `read disturb` as period vocabulary. Its background explains that a high voltage is applied to non-selected word lines during read so those cells conduct; this can put non-selected cells into a light-programming condition, add floating-gate charge, raise threshold voltage, and eventually compromise the erased/programmed distinction. The disclosed design varies the non-selected-word-line voltage and makes a tradeoff explicit: lowering it can suppress disturb, while lowering it too far can make some cells fail to conduct correctly during read.

Primary source: <https://patents.google.com/patent/US20030137873A1/en>.

This is an earlier manufacturer-primary witness than the 2009-priority controller patent already used in this case. It is **not** evidence that Fujitsu first discovered read disturb or invented every later mitigation technique.

### Independent qualification witness — NASA/JPL, March 2008

Douglas Sheldon and Michael Freie's NASA/JPL **_Disturb Testing in Flash Memories_**, JPL Publication 08-7, treats read disturb as a NAND reliability and qualification problem. The report says manufacturers acknowledged disturb failures and supplied guidance, describes read disturb as a neighboring-cell/state problem within a block, and records a contemporary rule of thumb of roughly one million READ cycles per block for SLC and 100,000 for MLC. If that guidance had to be exceeded, it recommends moving data to another block and erasing the original block, restarting that block's read-disturb exposure cycle.

Institutional source: <https://nepp.nasa.gov/files/13582/07-100%20Sheldon_JPL%20Distrub%20Testing%20in%20Flash%20Mem.pdf>.

The same report supplies a valuable **negative result**. Program 8 performed 50k, 100k, 500k, and 1M page-read operations on a single page, yet the report states that no program-disturb or read-disturb failures were detected in the tested devices. Therefore the report's read-count figures are historical guidance, not universal physical thresholds.

"""
anchor = "## Historical vocabulary and record\n\n"
if "### Earlier manufacturer-primary witness — Fujitsu, 2002 priority / 2003 publication" not in s:
    if anchor not in s:
        raise SystemExit("Case52 historical anchor missing")
    s = s.replace(anchor, anchor + historical, 1)

negative = """### Recognized mechanism ≠ universal read-count failure threshold

The NASA/JPL 2008 result prevents an easy but incorrect upgrade from `read disturb exists` to `a fixed read count predicts failure`. The report used large read-count sequences and contemporary migration/erase guidance, yet its own tested devices did not reproduce a disturb failure.

Therefore:

> **read-disturb mechanism ≠ universal fixed read-count failure threshold**.

A practical threshold is qualified by device generation, process, wear, data pattern, temperature, voltage, ECC margin, and test/workload conditions.

"""
anchor = "### Read count can become a maintenance clock\n"
if "### Recognized mechanism ≠ universal read-count failure threshold" not in s:
    if anchor not in s:
        raise SystemExit("Case52 read-count anchor missing")
    s = s.replace(anchor, negative + anchor, 1)

metadata = """### Compact maintenance summaries can govern much larger payloads

Cai et al.'s proposed `Vpass Tuning` implementation gives one bounded research example: one byte per block for the tuned `Vpass` setting and one byte for the predicted worst-case page. For the paper's assumed 512GB / 65,536-block configuration, that is 128KB total metadata.

This is a proposal/evaluation cost estimate, not a universal commercial SSD format. Its narrower methodological result is:

> **small maintenance metadata ≠ small retention significance**.

A controller can retain a counter, tuned setting, error-margin estimate, or worst-case-page summary without retaining a complete read history, yet that small control state can still govern when future reads remain safe.

"""
anchor = "### Recovery can use additional disturbance as diagnostic evidence\n"
if "### Compact maintenance summaries can govern much larger payloads" not in s:
    if anchor not in s:
        raise SystemExit("Case52 RDR anchor missing")
    s = s.replace(anchor, metadata + anchor, 1)

boundary = """### Boundary with Case 67 — later 3-D NAND adaptive read reclaim

Case 52 remains the canonical physical/access-induced read-disturb case and now carries the 2002–2015 historical bridge. Case 67 remains a distinct later controller-policy slice: a 2017-priority / 2019 SK hynix disclosure uses compressed read-count proxies, thresholded ECC qualification, adaptive checking, 3-D neighborhood sampling, and conditional reclaim. The shared trigger family does not make the controller policies historically or technically identical.

> **generic read-disturb mechanism/history ≠ one later 3-D NAND controller policy**.

"""
anchor = "## Read semantics compared with magnetic core\n"
if "### Boundary with Case 67 — later 3-D NAND adaptive read reclaim" not in s:
    if anchor not in s:
        raise SystemExit("Case52 comparison anchor missing")
    s = s.replace(anchor, boundary + anchor, 1)

CASE52.write_text(s)

# --- Evidence 52 -----------------------------------------------------------
s = EVID52.read_text()
s = s.replace("# Case 52 Grounding Record — NAND Read Disturb, 2009–2015", "# Case 52 Grounding Record — NAND Read Disturb, 2002–2015", 1)

note = """## Consolidation note

The grounding-record filename is retained for stable links, but the evidence window is now **2002–2015**. The former Case 97 duplicated Case 52's central mechanism. Its unique evidence has been absorbed here: Fujitsu's 2002-priority manufacturer filing and NASA/JPL's 2008 qualification/test report, including the explicit no-disturb-failure result. Git history retains the former files for provenance. Case 67 remains a separate later 3-D NAND controller-policy case.

"""
anchor = "## Evidence classes\n"
if "## Consolidation note" not in s:
    if anchor not in s:
        raise SystemExit("Evidence52 evidence-classes anchor missing")
    s = s.replace(anchor, note + anchor, 1)

rows = """| Fujitsu, US20030137873A1 / US6707714B2 | priority 2002-01-22; publication 2003-07-24 | manufacturer primary patent | early explicit NAND `read disturb` vocabulary; non-selected-word-line read voltage; light-programming / threshold-shift mechanism; voltage tradeoff | first discovery/invention priority; universal later-controller implementation |
| Sheldon & Freie, NASA/JPL Publication 08-7 | March 2008 | institutional qualification/test report | disturb as a reliability concern; migration+erase guidance; 50k/100k/500k/1M read protocol; explicit no-disturb-failure result | universal read-count threshold; evidence that the tested devices failed from read disturb |
"""
if "| Fujitsu, US20030137873A1 / US6707714B2 |" not in s:
    sep = "| --- | --- | --- | --- | --- |\n"
    if sep not in s:
        raise SystemExit("Evidence52 table separator missing")
    s = s.replace(sep, sep + rows, 1)

sections = """## Earlier manufacturer-primary evidence — Fujitsu 2002/2003

Fujitsu Limited, **“Read disturb alleviated flash memory,”** US20030137873A1 / US6707714B2:

- priority: 22 January 2002;
- U.S. filing: 22 October 2002;
- U.S. application publication: 24 July 2003;
- original assignee: Fujitsu Ltd.

Source: <https://patents.google.com/patent/US20030137873A1/en>.

The patent directly supports the date and historical vocabulary, NAND non-selected-word-line read-voltage stress, a light-programming / threshold-rise mechanism, and a disturb-versus-read-margin voltage tradeoff. It does **not** establish first discovery or universal later-controller implementation.

## Independent institutional qualification evidence — NASA/JPL 2008

Douglas Sheldon and Michael Freie, **_Disturb Testing in Flash Memories_**, JPL Publication 08-7, March 2008, NASA Electronic Parts and Packaging (NEPP) Program.

Source: <https://nepp.nasa.gov/files/13582/07-100%20Sheldon_JPL%20Distrub%20Testing%20in%20Flash%20Mem.pdf>.

The executive summary defines disturb testing around nearby programming/reading changing an expected state, states that manufacturers acknowledged disturb failures, and says no specific disturb failures were noted in the report's testing. The report gives contemporary SLC/MLC read-count guidance plus migration+erase mitigation; Program 8 performs 50k, 100k, 500k, and 1M page reads on one page; the conclusions report no program-disturb or read-disturb failures in the tested devices.

Evidence strength: **H/S — strong institutional qualification/test witness and especially strong as a negative-result boundary.** The numerical guidance is retained as 2008 guidance, not a universal NAND law.

> **recognized failure mechanism + conservative guidance ≠ a fixed failure threshold reproduced by every tested device**.

"""
anchor = "## Primary paper inspected\n"
if "## Earlier manufacturer-primary evidence — Fujitsu 2002/2003" not in s:
    if anchor not in s:
        raise SystemExit("Evidence52 primary-paper anchor missing")
    s = s.replace(anchor, sections + anchor, 1)

EVID52.write_text(s)

# --- README ---------------------------------------------------------------
s = README.read_text()
case52_line = "- [`cases/52-nand-flash-read-disturb-access-induced-decay.md`](cases/52-nand-flash-read-disturb-access-induced-decay.md) — grounded canonical NAND read-disturb case, now deepened across 2002–2015: Fujitsu 2002-priority manufacturer evidence, NASA/JPL 2008 qualification testing and negative-result evidence, pre-2015 controller/FTL prior art, and Cai et al. 2015 MLC characterization. It separates access-conditioned disturbance from retention-age loss and universal threshold claims; see [`evidence/52-cai-2009-2015-nand-read-disturb-grounding.md`](evidence/52-cai-2009-2015-nand-read-disturb-grounding.md)."
lines = []
replaced52 = False
for line in s.splitlines():
    if line.startswith("- [`cases/52-nand-flash-read-disturb-access-induced-decay.md`"):
        lines.append(case52_line)
        replaced52 = True
    elif "cases/97-nand-flash-read-disturb-access-conditioned-retention.md" in line or "evidence/97-nand-2002-2015-read-disturb-grounding.md" in line:
        continue
    else:
        lines.append(line)
if not replaced52:
    raise SystemExit("README Case52 line missing")
README.write_text("\n".join(lines) + "\n")

# --- ROADMAP --------------------------------------------------------------
s = ROADMAP.read_text()
roadmap_line = "- [x] NAND Flash read-disturb historical deepening / duplicate consolidation — canonical [`cases/52-nand-flash-read-disturb-access-induced-decay.md`](cases/52-nand-flash-read-disturb-access-induced-decay.md), using its stable [`evidence/52-cai-2009-2015-nand-read-disturb-grounding.md`](evidence/52-cai-2009-2015-nand-read-disturb-grounding.md) path, now absorbs the unique 2002–2008 evidence previously duplicated in Case 97: Fujitsu 2002-priority manufacturer evidence and NASA/JPL 2008 qualification testing, including the no-disturb-failure result. Case 67 remains the distinct later 3-D NAND adaptive-reclaim policy slice. Broader NAND/3D-NAND/controller genealogy, named commercial deployment, and device-specific threshold validation remain open and should be coordinated with `computing-archaeology`."
lines = []
replaced97 = False
for line in s.splitlines():
    if "cases/97-nand-flash-read-disturb-access-conditioned-retention.md" in line or "evidence/97-nand-2002-2015-read-disturb-grounding.md" in line:
        if not replaced97:
            lines.append(roadmap_line)
            replaced97 = True
        continue
    lines.append(line)
if not replaced97 and roadmap_line not in s:
    raise SystemExit("ROADMAP Case97 line missing")
ROADMAP.write_text("\n".join(lines) + "\n")

# --- CASE_INDEX -----------------------------------------------------------
s = INDEX.read_text()
case52_row = "| [NAND Flash Read Disturb: Access-Induced Decay, Vpass Mitigation, and Recovery](cases/52-nand-flash-read-disturb-access-induced-decay.md) | **grounded** | selected-page read + elevated `Vpass` on unselected same-block cells + cumulative read stress + threshold-voltage drift + ECC margin + optional compact maintenance metadata / relocation / RDR | separate present read success from future neighbor-retention cost; access-conditioned disturbance from retention-age refresh; selected-page nondestructiveness from zero material disturbance elsewhere; historical guidance from universal thresholds; measured chip behavior from proposed mitigation/recovery | [expanded 2002–2015 NAND read-disturb grounding](evidence/52-cai-2009-2015-nand-read-disturb-grounding.md); Case 67 covers later 3-D NAND adaptive read reclaim, while broader controller genealogy, named-product deployment, and independent fault validation remain separate work |"
lines = []
updated52 = False
for line in s.splitlines():
    if line.startswith("| [NAND Flash Read Disturb: Access-Induced Decay, Vpass Mitigation, and Recovery](cases/52-nand-flash-read-disturb-access-induced-decay.md)"):
        lines.append(case52_row)
        updated52 = True
    elif "cases/97-nand-flash-read-disturb-access-conditioned-retention.md" in line or "evidence/97-nand-2002-2015-read-disturb-grounding.md" in line:
        continue
    else:
        lines.append(line)
if not updated52:
    raise SystemExit("CASE_INDEX Case52 row missing")
s = "\n".join(lines) + "\n"
s = s.replace("| NAND read disturb / 2002–2015 bounded regime |", "| NAND read disturb / 2002–2015 bounded regime (Case 52 canonical) |", 1)
s = s.replace("### Case 97 — NAND Flash read-disturb findings", "### Case 52 historical deepening — 2002–2015 NAND Flash read-disturb findings", 1)
s = s.replace("Case 97 adds an access-triggered nonvolatile-memory regime", "the 2002–2015 Case 52 deepening adds an access-triggered nonvolatile-memory regime", 1)
for old, new in [
    ("96 bounded cases, 96 of them `grounded`", "95 bounded cases, 95 of them `grounded`"),
    ("96 bounded cases, all 96 `grounded`", "95 bounded cases, all 95 `grounded`"),
    ("96 canonical cases", "95 canonical cases"),
    ("96 bounded cases, 96 grounded", "95 bounded cases, 95 grounded"),
]:
    s = s.replace(old, new)
INDEX.write_text(s)

# Correct aggregate wording elsewhere if present.
for p in (README, ROADMAP):
    t = p.read_text()
    for old, new in [
        ("96 bounded cases, 96 of them `grounded`", "95 bounded cases, 95 of them `grounded`"),
        ("96 bounded cases, all 96 `grounded`", "95 bounded cases, all 95 `grounded`"),
        ("96 canonical cases", "95 canonical cases"),
        ("96 bounded cases, 96 grounded", "95 bounded cases, 95 grounded"),
    ]:
        t = t.replace(old, new)
    p.write_text(t)

# --- Remove duplicate current-tree files ---------------------------------
if CASE97.exists():
    CASE97.unlink()
if EVID97.exists():
    EVID97.unlink()

# --- Sanity checks --------------------------------------------------------
assert CASE52.exists() and EVID52.exists()
assert not CASE97.exists() and not EVID97.exists()
assert "Fujitsu, 2002 priority / 2003 publication" in CASE52.read_text()
assert "NASA/JPL, March 2008" in CASE52.read_text()
assert "# Case 52 Grounding Record — NAND Read Disturb, 2002–2015" in EVID52.read_text()
assert "NASA/JPL 2008" in EVID52.read_text()
assert len(list(Path("cases").glob("*.md"))) == 95

for p in Path(".").rglob("*.md"):
    t = p.read_text(errors="replace")
    if "cases/97-nand-flash-read-disturb-access-conditioned-retention.md" in t or "evidence/97-nand-2002-2015-read-disturb-grounding.md" in t:
        raise SystemExit(f"stale duplicate reference remains in {p}")

idx = INDEX.read_text()
assert "### Case 52 historical deepening — 2002–2015 NAND Flash read-disturb findings" in idx
assert "| NAND read disturb / 2002–2015 bounded regime (Case 52 canonical) |" in idx
