from pathlib import Path

CASE = Path("cases/36-nand-flash-correct-and-refresh-maintenance.md")
ROADMAP = Path("ROADMAP.md")
INDEX = Path("CASE_INDEX.md")

case_path = "cases/36-nand-flash-correct-and-refresh-maintenance.md"
grounding_path = "evidence/36-cai-2012-flash-correct-refresh-grounding.md"
prior_path = "evidence/36-flash-refresh-1997-2009-prior-art-deepening.md"

# --- Case 36 ---
case = CASE.read_text(encoding="utf-8")
old_status = "**`grounded`** — bounded to Yu Cai et al.'s peer-reviewed 2012 ICCD proposal and evaluation of **Flash Correct-and-Refresh (FCR)** for 3x-nm MLC NAND Flash, with later 2015 retention-characterization work used only as a boundary check on retention-age/read-recovery semantics."
new_status = old_status + " The historical novelty boundary is additionally deepened by pre-2012 nonvolatile-memory refresh patent records from 1997–2009; those records narrow what can safely be attributed to FCR without changing the case's bounded 2012 object."
if new_status not in case:
    if old_status not in case:
        raise SystemExit("Case 36 status anchor not found")
    case = case.replace(old_status, new_status, 1)

if prior_path not in case:
    anchor = f"Grounding record: [`../{grounding_path}`](../{grounding_path})."
    replacement = anchor + f"\n\nPrior-art deepening: [`../{prior_path}`](../{prior_path})."
    if anchor not in case:
        raise SystemExit("Case 36 grounding link anchor not found")
    case = case.replace(anchor, replacement, 1)

prior_section = """## Prior art and anti-anachronism

The 2012 paper includes a bounded authorial priority statement (“to our knowledge”) about its combination of retention-error characteristics. A dedicated prior-art deepening now makes the repository's boundary much firmer: [`../evidence/36-flash-refresh-1997-2009-prior-art-deepening.md`](../evidence/36-flash-refresh-1997-2009-prior-art-deepening.md) documents public pre-2012 records for several mechanisms that must **not** be treated as FCR inventions.

A 1997-filed / 1999-public U.S. patent already describes multilevel nonvolatile-memory refresh in response to threshold-voltage drift/error evidence, including ECC participation, deferred/idle-time refresh, periodic timer-driven refresh, retained last-refresh time, power-up refresh, and sector buffer→erase→rewrite. A separate 2000-filed / 2002-public Flash patent family describes dynamic refresh that can move data to a different physical location while an address-mapping circuit changes the logical/virtual→physical mapping. A 2005-public record describes age/timestamp-triggered in-place or out-of-place Flash refresh, and a 2007-filed / 2009-public record describes erase-free reprogram refresh triggered by elapsed time, level drift, or read-error evidence.

Therefore the repository rejects all of the following as FCR novelty claims:

- `generic nonvolatile-memory refresh first appears in FCR`;
- `periodic / idle-time / power-up Flash refresh first appears in FCR`;
- `ECC/error-assisted refresh first appears in FCR`;
- `refresh-time relocation/remapping first appears in FCR`;
- `retention-age/timestamp-triggered Flash refresh first appears in FCR`;
- `erase-free reprogram refresh first appears in FCR`.

The surviving bounded distinction is narrower: Cai et al. combine measured 3x-nm MLC retention-error characterization with explicit storage-time / P/E-wear / ECC trade-offs, remapping and in-place paths, hybrid fallback for the opposite/right-shift error population, per-block P/E-cycle-driven adaptive refresh rate, and SSD/workload simulation that makes the maintenance/endurance trade-off quantitative.

This is a **combination/evaluation boundary**, not an invention-priority judgment. Patent filing/priority date is also kept separate from public publication date. Patent disclosure does not prove commercial deployment, and functional similarity does not prove a patent-family → FCR design genealogy.

Nor does this project project the FCR term backward onto the earlier records. Their own terms — `refresh`, `dynamic refresh`, `refresh timer`, `address mapping`, `storage date`, and `rewrite refresh` — remain historical vocabulary. `FCR` is used historically only for the 2012 proposal and its later descendants/citations where explicitly sourced.

A 2015 follow-up by Cai et al. characterizes retention age in real 2y-nm MLC NAND and shows that optimal read-reference voltage changes with retention age. That later evidence deepens the general point that retained charge, readable interpretation, and controller recovery parameters can diverge over time. It is not used to rewrite either the pre-2012 patent mechanisms or the 2012 FCR mechanism, and it does not establish deployment.
"""
start_marker = "## Prior art and anti-anachronism\n"
end_marker = "\n## Functional analogy and philosophical limit"
start = case.find(start_marker)
end = case.find(end_marker, start)
if start < 0 or end < 0:
    raise SystemExit("Case 36 prior-art section anchors not found")
if prior_section not in case:
    case = case[:start] + prior_section.rstrip() + case[end:]

ledger_rows = """| Pre-2012 public records already describe periodic/deferred/power-up nonvolatile-memory refresh with error/ECC participation | H/P | US5909449A (1999 public record; 1997 filing) |
| Pre-2012 public records already describe refresh that relocates data and changes logical-to-physical mapping | H/P | US6396744B1 / 2000 priority family |
| Pre-2012 public records already describe age/timestamp-triggered in-place or out-of-place Flash refresh | H/P | US20050243626A1 / US7325090B2 |
| Pre-2012 public records already describe erase-free reprogram refresh triggered by time, drift, or read-error evidence | H/P | US20090161466A1 |
| Generic Flash refresh, refresh-time remapping, or erase-free rewrite refresh is an invention unique to FCR | X | contradicted by inspected pre-2012 patent records |
| Similarity between earlier patent mechanisms and FCR proves direct design genealogy or commercial deployment | X | neither influence chain nor shipped implementation is established by this slice |
"""
ledger_anchor = "| The reported 46× average lifetime improvement proves a production SSD achieved 46× measured field life | X |"
if ledger_rows not in case:
    pos = case.find(ledger_anchor)
    if pos < 0:
        raise SystemExit("Case 36 claim-ledger insertion anchor not found")
    case = case[:pos] + ledger_rows + case[pos:]

source_url = "https://patents.google.com/patent/US5909449A/en"
if source_url not in case:
    case = case.rstrip() + "\n" + """
5. Hock C. So and Sau C. Wong, **“Multibit-per-cell non-volatile memory with error detection and correction,”** US 5,909,449 A, filed 8 September 1997, public patent 1 June 1999: <https://patents.google.com/patent/US5909449A/en>.
6. **“Flash memory with dynamic refresh,”** US 6,396,744 B1, filed 25 April 2000, public patent 28 May 2002; same family includes relocation/address-mapping refresh records: <https://patents.google.com/patent/US6396744B1/en>.
7. **“Refreshing data stored in a flash memory,”** US 2005/0243626 A1 / US 7,325,090 B2, priority 29 April 2004, application publication 3 November 2005: <https://patents.google.com/patent/US7325090B2/en>.
8. Darlene G. Hamilton, Mark W. Randolph, Don Carlos Darling, Ron Kornitz, **“Extending flash memory data retension via rewrite refresh,”** US 2009/0161466 A1, filed 20 December 2007, published 25 June 2009: <https://patents.google.com/patent/US20090161466A1/en>.
""".lstrip() + "\n"
CASE.write_text(case, encoding="utf-8")

# --- ROADMAP ---
roadmap = ROADMAP.read_text(encoding="utf-8")
roadmap_entry = f"""- [x] Case 36 pre-FCR nonvolatile-Flash refresh prior-art boundary — [`{case_path}`]({case_path}), deepened by [`{prior_path}`]({prior_path}): 1997–2009 public patent records establish explicit refresh by threshold/error evidence, deferred/periodic/power-up scheduling, retained refresh-time state, refresh-time physical relocation plus logical→physical remapping, age/timestamp-triggered refresh, and erase-free rewrite refresh before Cai et al. 2012. The bounded FCR contribution is therefore narrowed to its measured 3x-nm MLC retention/wear/ECC policy combination, hybrid fallback, P/E-adaptive cadence, and evaluated SSD lifetime/endurance trade-off; patent disclosure != deployment and functional prior art != proven genealogy. Pre-1997 prior art, patent-prosecution genealogy, named commercial implementations, and broader controller history remain open and should primarily live in `computing-archaeology`."""
if prior_path not in roadmap:
    marker = "## Phase 2 — Build missing technical bridges\n\n"
    if marker not in roadmap:
        raise SystemExit("ROADMAP Phase 2 marker not found")
    roadmap = roadmap.replace(marker, marker + roadmap_entry + "\n", 1)
    ROADMAP.write_text(roadmap, encoding="utf-8")

# --- CASE_INDEX ---
index = INDEX.read_text(encoding="utf-8")
new_row = f"""| [NAND Flash Correct-and-Refresh: ECC-Bounded Retention Through Controller Maintenance]({case_path}) | **grounded** | nonvolatile MLC NAND + retention-error accumulation + ECC-corrected read + remap/in-place reprogram + adaptive controller scheduling | separate physical nonvolatility from maintenance-free reliable retention; show error-margin renewal can relocate state and consume endurance; bound FCR novelty against explicit 1997–2009 nonvolatile-refresh prior art | [2012 FCR grounding]({grounding_path}) + [1997–2009 refresh prior-art deepening]({prior_path}); commercial deployment, pre-1997 prior art, later 3D-NAND/read-retry interaction, vendor-specific refresh, and full controller genealogy remain separate work |"""
lines = index.splitlines()
row_hits = [i for i, line in enumerate(lines) if line.startswith("| [NAND Flash Correct-and-Refresh:") and case_path in line]
if len(row_hits) != 1:
    raise SystemExit(f"expected one Case 36 index row, found {len(row_hits)}")
lines[row_hits[0]] = new_row
index = "\n".join(lines)

findings = """## Case 36 — pre-FCR Flash-refresh prior-art deepening

- **1847 — 1997 filing != 1999 public disclosure:** US08/924,909 was filed 8 September 1997, while US5909449A became a public patent record on 1 June 1999; the filing date can bound priority-family chronology but must not be silently reported as the public-disclosure date. (`H/P`, `X`)
- **1848 — generic nonvolatile-memory refresh predates FCR:** the 1999 public record describes reading and reprogramming drifting multilevel nonvolatile state into allowed threshold-voltage ranges. (`H/P`)
- **1849 — deferred / periodic / idle-time / power-up refresh predates FCR:** the same record describes marking sectors for later refresh, timer-driven refresh, inactivity scheduling, retained last-refresh time, and power-up refresh. (`H/P`)
- **1850 — ECC/error evidence in refresh predates FCR:** the 1999 record explicitly allows error-detection/ECC information to identify corrected state during reading/refreshing; FCR did not originate the generic coupling of error evidence and renewal. (`H/P`, `X`)
- **1851 — refresh-time relocation/remapping predates FCR:** the 2000-filed / 2002-public dynamic-refresh family describes rewriting data to a different physical set while changing logical/virtual→physical address mapping. (`H/P`)
- **1852 — logical identity continuity across refresh != FCR-specific invention:** FCR's remapping path remains an important 2012 retention policy, but the bare idea that refresh can preserve a designation while replacing its physical embodiment already has earlier public technical prior art. (`H/P`, `E`, `X`)
- **1853 — data-age/timestamp-triggered Flash refresh predates FCR:** the 2005-public `Refreshing data stored in a flash memory` record describes in-place/out-of-place refresh based on storage age/timestamps, periodic events, boot/dismount, or data type. (`H/P`)
- **1854 — erase-free rewrite refresh predates FCR:** the 2007-filed / 2009-public Spansion record describes reprogramming stored Flash state without a full erase, with time, level-drift, or read-error triggers. (`H/P`)
- **1855 — earlier refresh functionality != commercial deployment:** a patent disclosure establishes a technical proposal/record, not that a named shipped SSD/controller implemented every disclosed mechanism. (`H/P`, `X`)
- **1856 — earlier functional prior art != proven patent→FCR genealogy:** similarity in refresh, remapping, timing, or reprogramming is insufficient to show that Cai et al. inherited, consulted, or implemented a particular patent family. (`A`, `X`)
- **1857 — FCR novelty boundary becomes combination/evaluation-specific:** the defensible 2012 distinction is the measured 3x-nm MLC retention-error regime coupled to storage-time/P-E-wear/ECC trade-offs, remap/in-place/hybrid alternatives, P/E-adaptive cadence, and quantified SSD/workload evaluation. (`H/P`, `E`)
- **1858 — historical `refresh` != one physical mechanism:** the earlier records include sector erase/rewrite, relocation/remapping, and erase-free reprogramming, while FCR adds its own bounded hybrid policy and DRAM refresh remains physically different; shared vocabulary does not erase mechanism differences. (`H/P`, `A`, `X`)
- **1859 — related-repository boundary:** current `tmzncty/computing-archaeology` search found no dedicated nonvolatile-Flash refresh patent/history case; Case 36 keeps the retention-specific novelty correction while broad patent/controller/commercial genealogy should move there if developed. (`H/P` project-state record)
"""
if "## Case 36 — pre-FCR Flash-refresh prior-art deepening" not in index:
    index = index.rstrip() + "\n\n" + findings.rstrip() + "\n"
INDEX.write_text(index, encoding="utf-8")

# --- invariants ---
case_final = CASE.read_text(encoding="utf-8")
roadmap_final = ROADMAP.read_text(encoding="utf-8")
index_final = INDEX.read_text(encoding="utf-8")
if case_final.count(prior_path) != 4:
    raise SystemExit(f"unexpected Case 36 prior-art path count: {case_final.count(prior_path)}")
if roadmap_final.count(prior_path) != 2:
    raise SystemExit(f"unexpected ROADMAP prior-art path count: {roadmap_final.count(prior_path)}")
if index_final.count(prior_path) != 1:
    raise SystemExit(f"unexpected CASE_INDEX prior-art path count: {index_final.count(prior_path)}")
if index_final.count("## Case 36 — pre-FCR Flash-refresh prior-art deepening") != 1:
    raise SystemExit("Case 36 prior-art findings heading missing or duplicated")
for n in range(1847, 1860):
    if index_final.count(f"**{n} —") != 1:
        raise SystemExit(f"finding {n} missing or duplicated")
