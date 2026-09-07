from pathlib import Path

roadmap = Path("ROADMAP.md")
case_index = Path("CASE_INDEX.md")

case_path = "cases/120-nvme14-endurance-group-scoped-health-history.md"
evidence_path = "evidence/120-nvme14-2019-endurance-group-grounding.md"

roadmap_text = roadmap.read_text(encoding="utf-8")
roadmap_entry = (
    f"- [x] NVMe 1.4 Endurance Group scoped health-history / hidden-media-work boundary — "
    f"[`{case_path}`]({case_path}), grounded by [`{evidence_path}`]({evidence_path}): "
    "the ratified 10 June 2019 Revision 1.4 and NVM Express's own change record make Endurance Groups an optional group-scoped endurance-management surface over one or more NVM Sets; the Endurance Group Information log separates current nonpersistent warning bits from cumulative/lifetime-qualified health/work fields and separately exposes host Data Units Written versus Media Units Written including controller work such as garbage collection. This closes only the bounded `namespace/NVM-Set scope vs Endurance-Group scope vs host-write history vs media-write history vs current warning/event state` relation; TP4018b/TP4050 proposal archaeology, broader pre-2019 endurance-domain prior art, exact field persistence/reconfiguration semantics, named multi-group controllers, nvme-cli traces, and independent FTL/media validation remain open.\n"
)
roadmap_anchor = "## Phase 2 — Build missing technical bridges\n\n"
if case_path not in roadmap_text:
    if roadmap_anchor not in roadmap_text:
        raise SystemExit("ROADMAP Phase 2 anchor not found")
    roadmap_text = roadmap_text.replace(roadmap_anchor, roadmap_anchor + roadmap_entry, 1)
roadmap.write_text(roadmap_text, encoding="utf-8")

index_text = case_index.read_text(encoding="utf-8")
case_row = (
    f"| [NVM Express 1.4 Endurance Groups: Scoped Wear History, Mixed-Lifetime Health State, and Hidden Media Work]({case_path}) | **grounded** | "
    "namespace payload + NVM Set membership + Endurance Group association + group-level spare/usage/endurance state + host/media-write counters + current nonpersistent warnings/events + hidden controller wear-management state | "
    "separate namespace/NVM-Set identity from endurance-history scope; host workload from media maintenance work; cumulative/lifetime state from current warning/event state; and host-visible group identity from physical wear-leveling geometry | "
    f"[2019 NVMe 1.4 grounding]({evidence_path}); TP4018b/TP4050 chronology, broader prior art, field-by-field persistence/reconfiguration, named multi-group controller validation, and physical FTL/NAND mapping remain separate work |\n"
)
case119_prefix = "| [DDR4 Post-Package Repair: Row-Address Continuity Across Spare-Row Substitution](cases/119-ddr4-post-package-repair-row-remapping.md)"
if case_path not in index_text:
    lines = index_text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.startswith(case119_prefix):
            lines.insert(i + 1, case_row)
            break
    else:
        raise SystemExit("CASE_INDEX Case 119 row anchor not found")
    index_text = "".join(lines)

old55 = "ATA SMART genealogy, JESD218 methodology, independent named-device calibration, modern telemetry/endurance-group evolution, and fleet policy remain separate work"
new55 = "ATA SMART genealogy, JESD218 methodology, independent named-device calibration, modern telemetry beyond Endurance Groups, and fleet policy remain separate work; NVMe 1.4 Endurance Group scope is now handled separately in Case 120"
if old55 in index_text:
    index_text = index_text.replace(old55, new55, 1)

index_text = index_text.replace(
    "currently ninety-four active canonical bounded cases (with intentional numbering gaps after duplicate consolidation)",
    "currently ninety-five active canonical bounded cases (with intentional numbering gaps after duplicate consolidation)",
    1,
)

findings_heading = "## Case 120 — NVMe 1.4 Endurance Group findings"
if findings_heading not in index_text:
    findings = r'''

## Case 120 — NVMe 1.4 Endurance Group findings

- **1910 — Revision 1.4 Endurance Groups != invention of retained storage-health history:** NVMe Revision 1.0 already supplies earlier controller-lifetime SMART/Health state; the 2019 contribution here is a new optional group scope over NVM Sets, not health telemetry as such. (`H/P`, `X`)
- **1911 — namespace identity != endurance-history scope:** a namespace is wholly contained in one NVM Set, while one Endurance Group may govern endurance across several NVM Sets and therefore several namespaces. (`H/P`, `E`)
- **1912 — NVM Set separation != Endurance Group separation:** Revision 1.4 calls NVM Sets logically and potentially physically separate but explicitly permits multiple sets to share one Endurance Group. (`H/P`, `E`)
- **1913 — logical/resource partition != physical wear-leveling partition:** NVMe explicitly places wear leveling, erases, and related NAND management below the interface, so Endurance Group identifiers cannot be read as die/channel/plane/block coordinates. (`H/P`, `E`, `X`)
- **1914 — group information lifetime != one uniform persistence class:** the Endurance Group log is described as information over the life of the group while its Critical Warning bits are explicitly current and nonpersistent. (`H/P`, `E`)
- **1915 — current warning != cumulative endurance history:** a present spare/reliability/read-only warning can clear/change independently of the larger usage/write/error history exposed for the group. (`H/P`, `E`)
- **1916 — event clear != wear reversal:** reading the Endurance Group Information log with RAE=0 may clear outstanding group events without any normative statement that spare capacity, accumulated writes, or physical wear are reset. (`H/P`, `E`)
- **1917 — host-written bytes != media-written bytes:** Revision 1.4 excludes internal controller writes such as garbage collection from Data Units Written while including host and controller writes in Media Units Written. (`H/P`, `E`)
- **1918 — media-write delta != exact garbage-collection ledger:** garbage collection is an explicit example of controller writes, but the interface does not provide a complete causal decomposition of all internal media work. (`H/P`, `X`)
- **1919 — logical mutation history != complete media-maintenance history:** controller relocation/maintenance can add media writes without a one-for-one host mutation, so endurance work can have a different history from application writes. (`E`)
- **1920 — Percentage Used != direct physical wear sensor:** the field is a vendor-specific estimate based on usage and predicted NVM life; the interface does not expose every cell's P/E count or retention margin. (`H/P`, `E`)
- **1921 — Percentage Used 100 != proven failure:** the standard explicitly allows estimated endurance to be consumed without necessarily indicating NVM failure, and the value may exceed 100. (`H/P`, `X`)
- **1922 — Endurance Estimate != deterministic remaining-life counter:** it is an estimate of group-lifetime writable bytes under an explicit write-amplification-of-one assumption. (`H/P`, `E`)
- **1923 — life of Endurance Group != automatically life of controller:** the log introduction uses the group lifetime while the Error Information entry-count field explicitly uses controller lifetime for that group; one inferred reset epoch must not be imposed on all fields. (`H/P`, `E`)
- **1924 — Endurance Group existence != one populated NVM Set:** the log definition permits an Endurance Group to consist of zero or more NVM Sets, blocking an identity equation while leaving exact create/delete/reuse semantics open. (`H/P`, `E`, `X`)
- **1925 — Case 55 controller SMART ~= Case 120 group health only at a bounded functional/evolutionary level:** both expose health/endurance state, but controller scope and Endurance Group scope are different normative objects. (`A`, `X`)
- **1926 — Case 76 JESD218 qualification != live Endurance Group telemetry:** a test/rating contract over workload, TBW, error criteria, and power-off retention is not the same retained object as a running subsystem's group health log. (`A`, `X`)
- **1927 — Case 04 FTL behavior != inferred Endurance Group implementation:** mapped Flash supplies a lower-layer reason host and media work may diverge, but NVMe 1.4 deliberately abstracts the actual wear-leveling/erase-management mechanism. (`A`, `X`)
- **1928 — 2019 NVMe feature floor != generic endurance-pooling invention date:** the official change page establishes Revision-1.4 chronology and names TP4018b/TP4050, but broader ATA/SCSI/vendor/research prior art and proposal genealogy remain open. (`H/P`, `X`)
- **1929 — related-repository boundary:** the current `tmzncty/computing-archaeology` tree has no dedicated NVMe Endurance Group case to reuse; broad SSD wear-leveling/resource-pool genealogy belongs there if developed, while Case 120 keeps the retention-specific scope/history decomposition. (`H/P` project-state record)
'''
    index_text = index_text.rstrip() + findings + "\n"

case_index.write_text(index_text, encoding="utf-8")

# Defensive integration checks.
for path in (Path(case_path), Path(evidence_path)):
    if not path.exists():
        raise SystemExit(f"missing research file: {path}")
for path in (roadmap, case_index):
    text = path.read_text(encoding="utf-8")
    if case_path not in text or evidence_path not in text:
        raise SystemExit(f"navigation missing Case 120 links in {path}")
if "**1910 —" not in index_text or "**1929 —" not in index_text:
    raise SystemExit("Case 120 findings range incomplete")
