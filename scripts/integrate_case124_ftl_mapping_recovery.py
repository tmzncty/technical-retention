from pathlib import Path

CASE_ROW = "| [FTL Power-Loss Mapping Recovery: Persistent Payload, Volatile Resolution State, and Reconstruction](cases/124-ftl-power-loss-mapping-recovery.md) | **grounded** | nonvolatile Flash payload + volatile working map/cache + Flash-resident mapping/allocation/checkpoint/log evidence + post-crash relation reconstruction | expose relation-loss as a forgetting/recovery mode: payload can survive while logical legibility/currentness depends on rebuilding L2P/BMT state; separate mapping reconstruction from payload reconstruction and SSD write-durability handoff | [1995–2014 mapping-recovery grounding](evidence/124-ftl-1995-2014-mapping-recovery-grounding.md); named shipping-controller firmware, exact crash ordering, and independent power-cut validation remain open |"

FINDINGS = r'''## Case 124 — FTL power-loss mapping-recovery findings

- **2029 — nonvolatile Flash ≠ nonvolatile runtime mapping:** the substrate can preserve payload across power loss while SRAM/DRAM-resident address-translation state disappears. (`H/P`, `H/S`, `E`)
- **2030 — payload survival ≠ logical legibility:** readable physical pages do not by themselves tell a restarted mapped store which page should answer a logical address. (`E`)
- **2031 — volatile working-map loss ≠ permanent relation loss:** Ban/Intel, Park et al., and the ITRI disclosure all provide bounded paths in which nonvolatile mapping/allocation evidence regenerates volatile lookup state. (`H/P`, `H/S`, `E`)
- **2032 — working lookup ≠ recovery substrate:** cache-resident BMT/page-table state serves normal lookup, while Flash-resident map blocks, spare-area metadata, checkpoints, or update logs can preserve the reconstruction basis. (`H/P`, `H/S`, `E`)
- **2033 — mapping reconstruction ≠ payload reconstruction:** rebuilding L2P/BMT/currentness state restores the relation used to find surviving data; it does not mathematically regenerate missing user bytes as RAID/EC reconstruction does. (`E`, `A`)
- **2034 — startup scan/replay ≠ payload rewrite:** scanning map metadata or replaying a mapping log can restore service metadata without rewriting every retained user page. (`H/P`, `H/S`, `E`)
- **2035 — mapping recovered ≠ payload validated:** a correct relation cannot prove that the selected NAND page is readable, intact, or that a pre-crash write reached media. (`E`, `X`)
- **2036 — readable physical page ≠ current logical page:** out-of-place Flash can retain obsolete embodiments until reclamation; currentness requires mapping/allocation evidence in addition to byte presence. (`H/P`, `E`)
- **2037 — retained checkpoint ≠ sufficient crash-consistent mapping:** retaining some metadata is weaker than retaining enough ordered/version-qualified evidence to recover the intended mapping at the crash boundary. (`E`, `X`)
- **2038 — retained mapping summary ≠ complete operation history:** map blocks, BMT snapshots, logs, and deterministic replay evidence preserve enough relation state for a recovery design without necessarily retaining every host operation. (`H/P`, `H/S`, `E`)
- **2039 — media-retention interval ≠ recovery latency:** NAND payload may have survived throughout the outage while ordinary logical service remains unavailable during table reconstruction. (`E`)
- **2040 — less recovery scanning ≠ stronger payload durability:** a bounded scan/checkpoint/replay design can reduce startup work without changing the underlying NAND cell-retention guarantee. (`H/S`, `E`, `X`)
- **2041 — similar recovery objective ≠ one implementation genealogy:** Ban startup rebuild, 2009 map-block reconstruction, 2011 hierarchical map/log replay, and 2014 deterministic recovery are functionally comparable but no direct descent is established here. (`A`, `X`)
- **2042 — Case 04 constitutive mapping ≠ Case 124 mapping-failure recovery:** Case 04 grounds how mapping preserves logical identity across relocation; Case 124 grounds how that relation is regenerated after volatile lookup loss. (`A`)
- **2043 — Case 15 payload-handoff failure ≠ Case 124 mapping-recovery failure:** losing volatile staged write data before nonvolatile commit is different from losing the volatile lookup representation for payload that already survives in Flash. (`A`)
- **2044 — Synthesis 15 relation decomposition gains a failure witness:** designation, payload value, physical embodiment, and resolution relation can have different survival/recovery paths; Case 124 concretely isolates the resolution relation. (`A`, `E`)
- **2045 — FTL mapping/currentness ≠ distributed replica currentness:** Synthesis 16 supplies a useful analogy that relation loss can change logical survival while bytes remain, but no distributed-consensus or replica genealogy is implied. (`A`, `X`)
- **2046 — related-repository boundary:** current `tmzncty/computing-archaeology` searches found no dedicated FTL power-loss mapping-recovery case; broad controller/FTL genealogy belongs there if developed, while Case 124 retains only payload/mapping/recovery-state lifetime distinctions. (`H/P` project-state record)'''

ROADMAP_PHASE3_NEW = "- [x] Recovering from loss of mapping/allocation metadata (whose *relation* made older payloads current/legible). — grounded by [Case 124](cases/124-ftl-power-loss-mapping-recovery.md): mapped Flash can retain user pages while volatile lookup state disappears, then reconstruct logical-to-physical/currentness relations from Flash-resident map/allocation/checkpoint/log evidence. This closes the bounded `payload survival ≠ logical legibility`, `volatile working map ≠ recovery substrate`, and `mapping reconstruction ≠ payload reconstruction` relation; named shipping-controller fault behavior and broader FTL genealogy remain open."
ROADMAP_PHASE4_NEW = "- [x] loss of index or mapping metadata — grounded at the mapped-Flash/FTL layer by [Case 124](cases/124-ftl-power-loss-mapping-recovery.md): nonvolatile payload can outlive volatile lookup state, while retained map blocks/BMT/log/checkpoint evidence can make the relation reconstructible. Complete loss beyond the available reconstruction substrate, named-controller power-cut behavior, filesystem/database index loss, and forensic recovery remain open;"

roadmap_path = Path("ROADMAP.md")
roadmap = roadmap_path.read_text(encoding="utf-8")
lines = roadmap.splitlines()
phase3_done = False
phase4_done = False
for i, line in enumerate(lines):
    if "Recovering from loss of mapping/allocation metadata" in line:
        lines[i] = ROADMAP_PHASE3_NEW
        phase3_done = True
    if line.strip().startswith("- [ ] loss of index or mapping metadata") or line.strip().startswith("- [x] loss of index or mapping metadata"):
        lines[i] = ROADMAP_PHASE4_NEW
        phase4_done = True
if not phase3_done:
    raise SystemExit("ROADMAP Phase-3 mapping-loss marker not found")
if not phase4_done:
    raise SystemExit("ROADMAP Phase-4 index/mapping-loss marker not found")
roadmap_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

index_path = Path("CASE_INDEX.md")
index = index_path.read_text(encoding="utf-8")
if "cases/124-ftl-power-loss-mapping-recovery.md" not in index:
    anchor = "cases/123-ata6-device-configuration-overlay-capability-retention.md"
    anchor_pos = index.find(anchor)
    if anchor_pos < 0:
        raise SystemExit("Case 123 row anchor not found")
    line_end = index.find("\n", anchor_pos)
    if line_end < 0:
        raise SystemExit("Case 123 row line ending not found")
    index = index[:line_end + 1] + CASE_ROW + "\n" + index[line_end + 1:]
if "## Case 124 — FTL power-loss mapping-recovery findings" not in index:
    index = index.rstrip() + "\n\n" + FINDINGS + "\n"
else:
    index = index.rstrip() + "\n"
index_path.write_text(index, encoding="utf-8")

self_path = Path("scripts/integrate_case124_ftl_mapping_recovery.py")
workflow_path = Path(".github/workflows/integrate-case124-ftl-mapping-recovery.yml")
if self_path.exists():
    self_path.unlink()
if workflow_path.exists():
    workflow_path.unlink()
