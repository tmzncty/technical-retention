from pathlib import Path
import re

case_path = Path("cases/131-dell-perc-foreign-configuration-controller-replacement.md")
evidence_path = Path("evidence/131-dell-perc-2007-2011-foreign-configuration-grounding.md")
assert case_path.exists(), case_path
assert evidence_path.exists(), evidence_path

# ROADMAP
road_path = Path("ROADMAP.md")
road = road_path.read_text(encoding="utf-8")
assert "Case 131 — Dell PERC foreign configuration / controller replacement" not in road
phase2 = road.index("## Phase 2")
phase3 = road.index("## Phase 3", phase2)
segment = road[phase2:phase3]
case130_marker = "- [x] **Case 130 — LTO"
case130_pos = segment.index(case130_marker)
line_end = segment.index("\n", case130_pos)
insert_at = phase2 + line_end + 1
entry = (
    "- [x] **Case 131 — Dell PERC foreign configuration / controller replacement** — "
    "grounded from dated Dell PERC 6 firmware records and later Dell operational documentation: "
    "member disks can retain an importable array configuration after controller-current state disappears, "
    "while controller-local uncommitted write cache is a separate retained state; controller replacement "
    "recovery therefore does not imply failed-controller dirty-cache recovery.\n"
)
road = road[:insert_at] + entry + road[insert_at:]

lines = road.splitlines()
hits = [i for i, line in enumerate(lines) if "controller failure" in line.lower() and "[ ]" in line]
assert len(hits) == 1, hits
i = hits[0]
indent = lines[i][:len(lines[i]) - len(lines[i].lstrip())]
lines[i] = (
    indent
    + "- [ ] **controller failure** — substantially advanced at the RAID configuration/admissibility layer by Case 131: "
    "Dell PERC foreign configuration can survive on member disks and be imported after controller replacement, "
    "while controller-local uncommitted write cache remains a separate failure domain. Still open: "
    "failed-controller dirty-cache recovery, controller-NVRAM corruption, cross-generation/vendor metadata compatibility, "
    "encrypted-key loss, and fault-injection evidence."
)
road_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

# CASE_INDEX table row + findings
idx_path = Path("CASE_INDEX.md")
idx = idx_path.read_text(encoding="utf-8")
assert "cases/131-dell-perc-foreign-configuration-controller-replacement.md" not in idx
row_marker = "cases/130-lto-generational-compatibility-reader-obsolescence.md"
row_pos = idx.index(row_marker)
row_start = idx.rfind("\n", 0, row_pos) + 1
row_end = idx.index("\n", row_pos)
new_row = (
    "| [Dell PERC Foreign Configuration: Retained Array Topology Across Controller Replacement]"
    "(cases/131-dell-perc-foreign-configuration-controller-replacement.md) | **grounded** | "
    "disk-resident array configuration + controller-current admissibility + controller-local preserved write cache | "
    "separate payload/media survival from controller admission; split configuration recovery from dirty-cache recovery and integrity maintenance | "
    "[2007–2011 grounding](evidence/131-dell-perc-2007-2011-foreign-configuration-grounding.md); earlier RAID-metadata/controller genealogy, "
    "failed-controller dirty-cache recovery, cross-generation compatibility, and fault injection remain open |"
)
idx = idx[:row_end + 1] + new_row + "\n" + idx[row_end + 1:]

ids = [int(x) for x in re.findall(r"\*\*(\d{4})\s+—", idx)]
assert ids and max(ids) == 2330, max(ids) if ids else None

block = r'''

## Case 131 — Dell PERC foreign configuration / controller replacement

- **2331 — PERC foreign configuration retains array-definition state, not the user payload itself.** Dell's dated firmware records and later operational docs describe foreign configuration as configuration/data on physical disks used to recognize/import virtual disks; payload/parity embodiments remain a separate state class. (`H/P`, `H/S`, `E`)
- **2332 — Physical-disk survival ≠ virtual-disk service availability.** Disks can remain present and readable while the controller refuses ordinary service because their configuration is foreign to its current admitted state. (`H/P`, `E`)
- **2333 — Disk-resident array configuration ≠ controller-current admitted configuration.** Remove/reinsert behavior shows that retained disk configuration can outlive the controller's current virtual-disk entry. (`H/P`, `E`)
- **2334 — Foreign configuration detected ≠ foreign configuration importable.** Dell's later member-sufficiency rules allow some degraded imports while rejecting insufficient RAID member sets. (`H/S`, `E`)
- **2335 — Configuration knowledge ≠ reconstructability.** A controller can know what a disk set claims to be without possessing enough surviving members to reconstruct or serve its payload. (`H/S`, `E`)
- **2336 — Configuration import ≠ RAID rebuild ≠ consistency verification.** Import re-admits the array relation; rebuild and parity/media checking remain separate obligations handled elsewhere in the repository. (`E`)
- **2337 — Import ≠ clear.** Dell treats import as re-establishing the old configuration relation and clear as removing the foreign relation so disks can be reused under another configuration path. (`H/P`, `E`)
- **2338 — Disk-resident foreign configuration ≠ controller-local uncommitted write cache.** The 2011 PERC 6/E record explicitly preserves dirty write-back cache in the controller while the disks separately carry the foreign configuration. (`H/P`, `E`)
- **2339 — Configuration re-admission ≠ pending-write commitment.** In the preserved-cache path, foreign import and the later cache flush are coupled but distinct transitions. (`H/P`, `E`)
- **2340 — Controller failure ≠ automatic payload/topology erasure.** Dell's controller-replacement guidance shows that surviving disk-resident configuration can permit a compatible replacement controller to recover the array relation. (`H/S`, `E`)
- **2341 — Controller replacement recovery ≠ failed-controller dirty-cache recovery.** The inspected 2011 source proves preserved cache on the controller experiencing missing disks, not transfer of dirty cache from a dead controller into its replacement. (`X`, `E`)
- **2342 — Disk-resident configuration survival ≠ arbitrary hot-migration safety.** Dell's 2007/2011 records require source-side shutdown for documented virtual-disk migration and warn against interrupting RAID-level migration/capacity expansion. (`H/P`, `E`)
- **2343 — Correct retained metadata ≠ safe operator choice.** Current Dell recovery guidance warns that importing a foreign disk at the wrong time can corrupt an otherwise active array. (`H/S`, `E`)
- **2344 — Array admission ≠ array integrity maintenance.** Case 131's import boundary precedes Case 102's Patrol Read / Consistency Check maintenance on an admitted PERC array. (`A`, `E`)
- **2345 — PERC foreign-config import and ZFS vdev-label/uberblock recovery are functional analogies only.** Both retain member-media metadata that can outlive controller/volatile state, but no common mechanism or genealogy is asserted. (`A`, `X`)
- **2346 — November 2007 is a directly evidenced Dell documentation floor, not an invention date.** Earlier PERC/MegaRAID, other hardware-RAID metadata formats, and controller-NVRAM genealogy remain open and are better suited to `computing-archaeology`. (`H/P`, `X`)
'''
idx = idx.rstrip() + block + "\n"
ids2 = [int(x) for x in re.findall(r"\*\*(\d{4})\s+—", idx)]
assert max(ids2) == 2346, max(ids2)
assert len(ids2) == len(set(ids2)), "duplicate finding IDs"
idx_path.write_text(idx, encoding="utf-8")
