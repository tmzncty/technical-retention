from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
roadmap_path = ROOT / "ROADMAP.md"
index_path = ROOT / "CASE_INDEX.md"
case89_path = ROOT / "cases/89-ata-lba-chs-translation-logical-sector-identity.md"
case113_path = ROOT / "cases/113-ata-atapi6-48bit-lba-reachability.md"
evidence113_path = ROOT / "evidence/113-ata-2000-2003-48bit-lba-grounding.md"

for p in [roadmap_path, index_path, case89_path, case113_path, evidence113_path]:
    if not p.exists():
        raise SystemExit(f"missing required file: {p.relative_to(ROOT)}")

# ROADMAP: close only the bounded LBA28->LBA48 reachability slice while
# preserving the broad HDD-history item as open.
roadmap = roadmap_path.read_text(encoding="utf-8")
case113_item = (
    "- [x] ATA/ATAPI-6 48-bit Address feature / legacy-reachability boundary — "
    "[`cases/113-ata-atapi6-48bit-lba-reachability.md`](cases/113-ata-atapi6-48bit-lba-reachability.md), "
    "grounded by [`evidence/113-ata-2000-2003-48bit-lba-grounding.md`](evidence/113-ata-2000-2003-48bit-lba-grounding.md): "
    "T13's 2000 proposal record and December-2001 ATA/ATAPI-6 working draft separate 28-bit command reach from the larger 48-bit LBA namespace while preserving legacy commands; "
    "Maxtor's 2003 DiamondMax16 supplies a named >137 GB product witness, and Seagate's 2003 support note separates drive capability from BIOS/controller/driver/OS reachability. "
    "This closes only the bounded `logical-sector population vs command-family reach vs host interpretation` relation; proposal/final-standard genealogy, BIOS/OS adoption, HPA/DCO, SATA/ACS, 4Kn/512e, controller internals, and fault reproduction remain open and belong primarily in `computing-archaeology`.\n"
)

if "cases/113-ata-atapi6-48bit-lba-reachability.md" not in roadmap:
    lines = roadmap.splitlines(keepends=True)
    target_i = next((i for i, line in enumerate(lines) if line.startswith("- [ ] HDD geometry, bad-sector remapping, CHS → LBA")), None)
    if target_i is None:
        raise SystemExit("ROADMAP HDD broad item not found")
    lines.insert(target_i, case113_item)
    roadmap = "".join(lines)

# Update the broad HDD item's coverage summary without declaring it complete.
lines = roadmap.splitlines(keepends=True)
for i, line in enumerate(lines):
    if line.startswith("- [ ] HDD geometry, bad-sector remapping, CHS → LBA"):
        if "Cases 14, 89, and 108" in line:
            line = line.replace("Cases 14, 89, and 108", "Cases 14, 89, 108, and 113")
        elif "Cases 14, 89, 108, and 113" not in line:
            raise SystemExit("ROADMAP HDD case-summary shape changed")
        line = line.replace(" LBA28→LBA48,", "")
        lines[i] = line
        break
else:
    raise SystemExit("ROADMAP HDD broad item vanished")
roadmap = "".join(lines)
roadmap_path.write_text(roadmap, encoding="utf-8")

# CASE_INDEX navigation row + findings. Keep numbering collision-safe.
index = index_path.read_text(encoding="utf-8")
row = (
    "| [ATA/ATAPI-6 48-bit Address Feature: Reachability Beyond the 28-bit Ceiling](cases/113-ata-atapi6-48bit-lba-reachability.md) | **grounded** | "
    "logical sectors + legacy 28-bit reach + wider 48-bit EXT commands + capability/capacity descriptors + host-stack compatibility | "
    "distinguish logical-sector existence, command-family reachability, capability state, capacity reporting, and physical embodiment; show backward command interoperability need not preserve full-capacity reach | "
    "[2000–2003 grounding record](evidence/113-ata-2000-2003-48bit-lba-grounding.md); pre-2000 genealogy, final-standard revision archaeology, BIOS/OS chronology, HPA/DCO, SATA/ACS, 4Kn/512e, controller fault validation remain open |\n"
)

if "cases/113-ata-atapi6-48bit-lba-reachability.md) | **grounded**" not in index:
    lines = index.splitlines(keepends=True)
    anchor_i = next((i for i, line in enumerate(lines) if "cases/112-hbm3-rfm-bonus-maintenance-vs-periodic-refresh.md)" in line), None)
    if anchor_i is None:
        raise SystemExit("CASE_INDEX Case 112 navigation row not found")
    lines.insert(anchor_i + 1, row)
    index = "".join(lines)

findings_heading = "## Case 113 — ATA/ATAPI-6 48-bit LBA reachability findings"
if findings_heading not in index:
    nums = [int(x) for x in re.findall(r"(?:^|\n)(?:- \*\*)?(\d{4})(?:\s*—|\.| \*\*)", index)]
    max_num = max(nums) if nums else 0
    if max_num != 1765:
        raise SystemExit(f"finding-number collision risk: expected max 1765, found {max_num}")
    findings = """

## Case 113 — ATA/ATAPI-6 48-bit LBA reachability findings

- **1766 — device logical-sector population ≠ legacy command-family reach:** ATA/ATAPI-6 can report a 48-bit-addressable logical-sector range larger than the range encodable by legacy 28-bit commands; inability of one command family to name a high LBA does not prove that the logical sector is absent. (`H/P`, `E`)
- **1767 — 48-bit Address support ≠ retirement of 28-bit commands:** the 1410D working draft requires a device implementing the 48-bit feature to retain the 28-bit command family and permits 28-bit and 48-bit commands to be intermixed. (`H/P`)
- **1768 — 28-bit/48-bit coexistence ≠ two payload populations:** over the lower address range, the two command forms are alternative ways to designate sectors in one ATA logical-block service rather than evidence of independent stored datasets. (`E`)
- **1769 — legacy capacity descriptor ≠ whole 48-bit-addressable device capacity:** ATA/ATAPI-6 separates IDENTIFY DEVICE words 60–61 from words 100–103 so a sufficiently large device can expose the legacy ceiling and a larger 48-bit range simultaneously. (`H/P`)
- **1770 — capacity field value ≠ feature-support evidence:** the draft assigns 48-bit feature support to the defined IDENTIFY capability bit rather than telling hosts to infer support solely from the reported capacity values. (`H/P`)
- **1771 — legacy native-max result ≠ physical native-capacity ceiling:** on a device whose native maximum exceeds the legacy range, the non-EXT maximum-address command can return the legacy ceiling while its EXT counterpart addresses the larger regime. (`H/P`, `E`)
- **1772 — backward command compatibility ≠ backward full-capacity reachability:** preserving old commands allows older operations over their representable range but cannot make a 28-bit command encode a high LBA. (`E`)
- **1773 — wider LBA encoding ≠ physical-sector relocation:** the 48-bit feature extends host command/address parameters; the inspected contract does not state that introducing or using the wider form moves existing user sectors on the medium. (`E`, `X`)
- **1774 — wider LBA encoding ≠ exposed platter geometry:** ATA/ATAPI-6's wider form remains LBA-only; Cases 89 and 108 separately establish that logical addressing and physical ZBR geometry are distinct layers. (`H/P`, `A` bounded only)
- **1775 — 48-bit address width ≠ logical/physical-sector-size transition:** this case changes numeric address reach and command parameter width, not the 512e/4Kn relation or later logical/physical sector-size reporting. (`E`, `X`)
- **1776 — device-side 48-bit support ≠ end-to-end host-stack reachability:** Seagate's 2003 guidance requires compatible system software and, in relevant configurations, BIOS/controller support to use >137 GB capacity safely. (`H/P` bounded ecosystem claim)
- **1777 — address-interpretation failure ≠ magnetic-retention failure:** Seagate's Windows-specific wraparound warning shows that retained media can be overwritten through an incompatible addressing path; the failure is not evidence that the original magnetic state first decayed on its own. (`H/P`, `E` bounded to the documented configurations)
- **1778 — Cases 14/89/108/113 are a layer decomposition, not one remapping mechanism:** physical defect replacement, logical CHS representation, ZBR physical geometry, and command-address reach solve different problems beneath/around logical-block service. (`A` functional comparison only)
- **1779 — January-2000 proposal / December-2001 draft ≠ invention or final-standard priority:** T13's proposal index is a public standards-development floor; revision 3a labels itself an internal working document, while T13 separately lists INCITS 361-2002. (`H/P`, `X`)
- **1780 — related-repository boundary:** searches of `tmzncty/computing-archaeology` for `LBA48`, `48-bit LBA`, and `ATA-6` returned no dedicated case to reuse; broad ATA/BIOS capacity-barrier history should be developed there, while Case 113 keeps only the retention-specific reachability boundary. (`H/P` project-state record)
"""
    index = index.rstrip() + findings + "\n"
index_path.write_text(index, encoding="utf-8")

# Case 89 continuation: coordinate representation and command-width reach are
# intentionally separate axes.
case89 = case89_path.read_text(encoding="utf-8")
continuation_heading = "## Continuation — Case 113 48-bit address-width expansion"
if continuation_heading not in case89:
    continuation = """

---

## Continuation — Case 113 48-bit address-width expansion

[Case 113](113-ata-atapi6-48bit-lba-reachability.md) closes a different address-retention axis left open here. Case 89 shows that **one logical sector can keep the same LBA while its logical-CHS representation changes**. Case 113 shows that **one ATA logical-block namespace can outgrow the numeric reach of the legacy 28-bit command family while a wider 48-bit command family coexists with it**.

The comparison is deliberately bounded:

> **coordinate-representation continuity ≠ command-address-width reachability**

and:

> **ATA-2/ATA-3 translation → ATA/ATAPI-6 48-bit chronology ≠ proof that all physical placement or capacity-history mechanisms form one genealogy**.

Case 108 remains the physical ZBR counterpart and Case 14 remains the failure-triggered physical-reassignment counterpart.
"""
    case89 = case89.rstrip() + continuation + "\n"
case89_path.write_text(case89, encoding="utf-8")

print("Case 113 navigation/status integration prepared")
