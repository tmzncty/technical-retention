import re
from pathlib import Path

ROADMAP = Path("ROADMAP.md")
INDEX = Path("CASE_INDEX.md")
CASE54 = Path("cases/54-ddr5-rfm-split-maintenance-authority.md")

case_path = "cases/118-micron-ddr5-directed-refresh-management.md"
evidence_path = "evidence/118-micron-2012-2024-ddr5-drfm-grounding.md"

# --- Case 54 continuation ---
case54 = CASE54.read_text(encoding="utf-8")
continuation = (
    "Directed spatial continuation: [`118-micron-ddr5-directed-refresh-management.md`]"
    "(118-micron-ddr5-directed-refresh-management.md) now grounds a named Micron DDR5 DRFM product contract "
    "in which a sampled row address anchors a BRC-bounded physical-neighbor refresh set; this is separate from "
    "Case 54's bank-level RAA/RFM split-authority relation."
)
if "118-micron-ddr5-directed-refresh-management.md" not in case54:
    anchor = "Grounding record: [`../evidence/54-ddr5-rfm-2022-2025-grounding.md`](../evidence/54-ddr5-rfm-2022-2025-grounding.md)."
    if anchor not in case54:
        raise SystemExit("Case 54 grounding anchor not found")
    case54 = case54.replace(anchor, anchor + "\n\n" + continuation, 1)
    CASE54.write_text(case54, encoding="utf-8")

# --- ROADMAP ---
roadmap = ROADMAP.read_text(encoding="utf-8")
roadmap_entry = (
    f"- [x] Micron DDR5 Directed Refresh Management / sampled-row physical-neighbor boundary — "
    f"[`{case_path}`]({case_path}), grounded by [`{evidence_path}`]({evidence_path}): Micron's 16Gb DDR5 "
    "Die Rev D Rev. E (01/2024) product contract separates the DRFM sampled address from the physically adjacent "
    "rows actually refreshed, makes BRC2/3/4 a configurable bounded neighbor distance, permits nonuniform "
    "outer-row refresh ratios, and couples broader BRC scope to longer product-specific tDRFM. Intel's "
    "2012-priority row-hammer targeted-refresh record supplies earlier address-directed adjacent-victim prior art "
    "without proving a direct genealogy into DDR5 DRFM. This closes only the bounded sampled-address / hidden "
    "physical-neighbor / BRC / timing relation; exact JEDEC DRFM adoption chronology, sampled-address generation, "
    "ARFM/PRAC interaction, named-controller traces, internal remapping, and independent fault validation remain open."
)
if case_path not in roadmap:
    marker = "## Phase 2 — Build missing technical bridges\n\n"
    if marker not in roadmap:
        raise SystemExit("ROADMAP Phase 2 marker not found")
    roadmap = roadmap.replace(marker, marker + roadmap_entry + "\n", 1)

old_count = "**partially advanced by thirteen grounded bounded sub-slices**"
new_count = "**partially advanced by fourteen grounded bounded sub-slices**"
if old_count in roadmap:
    roadmap = roadmap.replace(old_count, new_count, 1)
elif new_count not in roadmap:
    raise SystemExit("DRAM bounded-sub-slice count anchor not found")

dram_clause = (
    f" [`{case_path}`]({case_path}), grounded by [`{evidence_path}`]({evidence_path}), adds the directed spatial "
    "sub-slice: one sampled row address can anchor restoration of a device-resolved bounded set of physically adjacent "
    "neighbors, while BRC radius, outer-row refresh ratio, bank-level command scope, and maintenance duration remain "
    "separate relations; Intel's 2012-priority targeted-refresh record blocks an origin claim without establishing "
    "Intel→DDR5 genealogy."
)
if "adds the directed spatial sub-slice" not in roadmap:
    anchor = " The broad item stays unchecked because a true JEDEC standards chronology"
    if anchor not in roadmap:
        raise SystemExit("DRAM broad-item continuation anchor not found")
    roadmap = roadmap.replace(anchor, dram_clause + anchor, 1)

ROADMAP.write_text(roadmap, encoding="utf-8")

# --- CASE_INDEX row ---
index = INDEX.read_text(encoding="utf-8")
row = (
    f"| [Micron DDR5 Directed Refresh Management: Sampled-Row Authority and Bounded Physical-Neighbor Refresh]({case_path}) "
    f"| **grounded** | DDR5 payload + sampled row address + device-internal physical-neighbor relation + BRC2/3/4 "
    "bounded radius + distance-dependent refresh ratio + DRFMab/DRFMsb timing | separate maintenance anchor from "
    "refreshed-row set; visible address from hidden physical adjacency; BRC coverage from equal refresh frequency; "
    "bank command scope from row-neighbor radius; manufacturer contract from empirical immunity | "
    f"[2012–2024 grounding]({evidence_path}); exact JEDEC DRFM genealogy, sample-generation rules, ARFM/PRAC interaction, "
    "controller traces, internal remapping, cross-vendor comparison, and fault injection remain open |"
)
if case_path not in index:
    lines = index.splitlines()
    hits = [i for i, line in enumerate(lines) if line.startswith("| [Apache HDFS Startup Safemode:") and "cases/117-apache-hdfs-startup-safemode-reobservation.md" in line]
    if len(hits) != 1:
        raise SystemExit(f"expected one Case 117 table row, found {len(hits)}")
    lines.insert(hits[0] + 1, row)
    index = "\n".join(lines)

# --- CASE_INDEX findings ---
heading = "## Case 118 — Micron DDR5 Directed Refresh Management findings"
claims = [
    "**Micron product DRFM != invention-priority proof:** the January-2024 16Gb DDR5 Die Rev D addendum is a named product contract and public product-era floor, not evidence that Micron or DDR5 invented targeted neighbor refresh. (`H/P`, `X`)",
    "**DRFM sampled address != refreshed-row set:** the product contract directs maintenance from a sampled row while stating that physically adjacent neighboring rows are the rows refreshed. (`H/P`, `E`)",
    "**visible/sampled row designation != disclosed physical-neighbor map:** the later product wording plus earlier Intel targeted-refresh prior art preserve a split in which the device can resolve physical adjacency hidden from ordinary controller-visible address ordering. (`H/P`, `E`)",
    "**BRC radius != physical vulnerability proof:** BRC2/3/4 bounds the configured directed-refresh neighborhood; it does not independently demonstrate that every vulnerable physical relation under every disturbance pattern lies inside that radius. (`H/P`, `X`)",
    "**inside BRC radius != refreshed on every DRFM command:** Micron always refreshes ±1 while rows farther away can be refreshed according to a DRAM-controlled ratio. (`H/P`)",
    "**maintenance coverage != uniform maintenance frequency:** one configured spatial set can contain members with different restoration cadence. (`E`)",
    "**BRC breadth != zero-cost protection:** for the inspected product, tDRFM grows with BRC according to `(2 * tRRF) * BRC`, with larger tabulated command durations. (`H/P`, `E`)",
    "**product timing != universal DDR5 timing:** 280/420/560 ns DRFMab and 240/360/480 ns DRFMsb are bounded Micron product values, not cross-vendor laws. (`H/P`, `X`)",
    "**bank-level command scope != row-neighbor radius:** DRFMab/DRFMsb and BRC encode different spatial axes and must not be collapsed because both describe maintenance geometry. (`H/P`, `E`)",
    "**directed disturbance maintenance != ordinary periodic refresh:** the earlier targeted-refresh record explicitly treats targeted work as off-cycle; existing DDR5/HBM cases separately retain ordinary REF coverage/accounting. (`H/P`, `A`)",
    "**DRFM completion != disclosed internal algorithm:** the contract specifies bounded neighbor work/time but not complete internal remapping, detector, victim-selection, or ratio implementation. (`H/P`, `X`)",
    "**manufacturer DRFM contract != independent RowHammer immunity:** feature semantics and command timing are not a substitute for named-module fault injection under arbitrary patterns. (`H/P`, `X`)",
    "**2012-priority targeted-refresh record predates the 2024 product witness:** Intel's family already describes controller-provided address information followed by device-resolved adjacent-victim refresh. (`H/P`)",
    "**2012 priority != 2014 public publication:** the Intel family priority/filing date is 30 June 2012 while US20140006703A1 was published 2 January 2014. (`H/P`)",
    "**earlier targeted-refresh function != DDR5 DRFM terminology:** the older source uses `row hammer` / `targeted refresh` / `victim row`; `DRFM`, `sampled address`, and `BRC` remain later DDR5 vocabulary in this slice. (`H/P`, `X`)",
    "**earlier functional prior art != proven Intel→DDR5 genealogy:** chronological/mechanistic resemblance blocks an origin myth but does not establish direct standards or implementation descent. (`A`, `X`)",
    "**related-repository boundary:** current `computing-archaeology` searches for `Directed Refresh Management` and `DRFM` found no dedicated case, so Case 118 keeps the retention-specific relation while broader DDR5/RowHammer history remains routed there if developed. (`H/P` project-state record)",
]
if heading not in index:
    nums = [int(x) for x in re.findall(r"(?m)^- \*\*(\d+) —", index)]
    nums += [int(x) for x in re.findall(r"(?m)^(\d+)\. \*\*", index)]
    if not nums:
        raise SystemExit("could not find existing CASE_INDEX finding numbers")
    start = max(nums) + 1
    findings = [heading, ""]
    for offset, claim in enumerate(claims):
        findings.append(f"- **{start + offset} — {claim}")
    index = index.rstrip() + "\n\n" + "\n".join(findings) + "\n"

INDEX.write_text(index, encoding="utf-8")

# --- invariants ---
roadmap_final = ROADMAP.read_text(encoding="utf-8")
index_final = INDEX.read_text(encoding="utf-8")
case54_final = CASE54.read_text(encoding="utf-8")

if roadmap_final.count(case_path) < 3:
    raise SystemExit(f"unexpected ROADMAP Case 118 path count: {roadmap_final.count(case_path)}")
if index_final.count(case_path) != 1:
    raise SystemExit(f"unexpected CASE_INDEX Case 118 path count: {index_final.count(case_path)}")
if index_final.count(heading) != 1:
    raise SystemExit("Case 118 findings heading missing or duplicated")
if case54_final.count("118-micron-ddr5-directed-refresh-management.md") != 2:
    raise SystemExit("Case 54 continuation link missing or duplicated")
if new_count not in roadmap_final:
    raise SystemExit("DRAM bounded-sub-slice count not updated")

print("Case 118 integration prepared successfully")
