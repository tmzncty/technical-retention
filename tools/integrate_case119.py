from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
roadmap_path = ROOT / "ROADMAP.md"
index_path = ROOT / "CASE_INDEX.md"
case_path = ROOT / "cases/119-ddr4-post-package-repair-row-remapping.md"
evidence_path = ROOT / "evidence/119-ddr4-1979-2023-post-package-repair-grounding.md"

for path in (roadmap_path, index_path, case_path, evidence_path):
    if not path.exists():
        raise SystemExit(f"required path missing: {path.relative_to(ROOT)}")

roadmap = roadmap_path.read_text(encoding="utf-8")
index = index_path.read_text(encoding="utf-8")

roadmap_marker = "- [x] Micron DDR5 Directed Refresh Management / sampled-row physical-neighbor boundary"
roadmap_entry = "- [x] DDR4 Post-Package Repair row-address / spare-row / repair-state-lifetime boundary — [`cases/119-ddr4-post-package-repair-row-remapping.md`](cases/119-ddr4-post-package-repair-row-remapping.md), grounded by [`evidence/119-ddr4-1979-2023-post-package-repair-grounding.md`](evidence/119-ddr4-1979-2023-post-package-repair-grounding.md): Micron DDR4 product documentation plus Intel and Lenovo platform records separate non-persistent `sPPR` from persistent/permanent `hPPR`, show a failing row address being redirected to an internal spare row under firmware/controller authority, and expose finite repair resources. Intel's 2020-priority hard-PPR power-failure disclosure further shows that establishing persistent repair state can itself require a protected transition interval, while a 1979-filed spare-row/decoder patent supplies much earlier address-substitution prior art without proving direct genealogy. This closes only the bounded `logical row address vs physical row embodiment vs repair-state lifetime vs payload volatility vs repair-transition durability` relation; exact JEDEC adoption chronology, official Micron archival facsimile, cross-vendor fuse/antifuse implementations, target-row payload semantics, repair-resource exhaustion, and fault injection remain open."

if "cases/119-ddr4-post-package-repair-row-remapping.md" not in roadmap:
    pos = roadmap.find(roadmap_marker)
    if pos < 0:
        raise SystemExit("ROADMAP Case 118 anchor not found")
    roadmap = roadmap[:pos] + roadmap_entry + "\n" + roadmap[pos:]

row = "| [DDR4 Post-Package Repair: Row-Address Continuity Across Spare-Row Substitution](cases/119-ddr4-post-package-repair-row-remapping.md) | **grounded** | volatile DRAM payload + spare-row substitution + soft/hard repair mapping with different lifetimes | separate logical row designation, physical row embodiment, repair-state persistence, payload volatility, transition durability, and finite spare capacity | [1979–2023 grounding record](evidence/119-ddr4-1979-2023-post-package-repair-grounding.md); exact JEDEC adoption chronology, official Micron archive, cross-vendor repair implementation, target-row payload semantics, and fault injection remain open |"

if "cases/119-ddr4-post-package-repair-row-remapping.md" not in index:
    lines = index.splitlines()
    insert_at = None
    for i, line in enumerate(lines):
        if line.startswith("| [") and "cases/118-micron-ddr5-directed-refresh-management.md" in line:
            insert_at = i + 1
            break
    if insert_at is None:
        raise SystemExit("CASE_INDEX Case 118 table row anchor not found")
    lines.insert(insert_at, row)
    index = "\n".join(lines) + ("\n" if index.endswith("\n") else "")

nums = [int(x) for x in re.findall(r"(?:^|\n)- \*\*(\d+) —", index)]
if not nums:
    raise SystemExit("no modern finding numbers found")
max_num = max(nums)
if "## Case 119 — DDR4 Post-Package Repair findings" not in index:
    if max_num != 1863:
        raise SystemExit(f"expected existing max finding 1863, found {max_num}; refusing to renumber concurrently")
    findings = r'''

## Case 119 — DDR4 Post-Package Repair findings

- **1864 — DDR4 PPR != invention of redundant-row substitution:** Procyk/Cenker's 1979-filed semiconductor-memory patent already describes spare rows/columns taking over addresses of defective standard elements through programmable decoder changes. (`H/P`, `X`)
- **1865 — logical row-address continuity != physical-row continuity:** PPR can keep future accesses associated with a failing row address while redirecting them to an internal spare row. (`H/P`, `E`)
- **1866 — persistent hPPR mapping != nonvolatile DRAM payload:** the hard repair relation can remain across later boots/power cycles even though ordinary DRAM charge state still requires power and refresh. (`H/P`, `E`)
- **1867 — sPPR non-persistence != failed or incomplete hPPR:** Lenovo/Micron documentation treats soft repair as a distinct temporary/reversible lifetime class rather than merely a broken permanent repair. (`H/P`, `X`)
- **1868 — row remapping != demonstrated payload migration:** the inspected sources establish future address redirection but do not establish a universal copy of every current bit from the defective row into the spare row. (`H/P`, `E`, `X`)
- **1869 — PPR row substitution != ECC correction:** ECC can reconstruct a currently requested value while PPR changes which physical row future accesses select; detection/correction and embodiment retirement are separate relations. (`E`, `A`, `X`)
- **1870 — defect existence != defect evidence != repair authorization:** a faulty cell/row, evidence that identifies it, and the command/firmware decision to consume a spare row are different retained/control states. (`H/P`, `E`)
- **1871 — DRAM PPR capability != autonomous DRAM repair authority:** Intel's named platform path gives BIOS a role in identifying a failing row and invoking PPR; device capability alone does not prove all diagnosis/scheduling occurs inside the DRAM. (`H/P`)
- **1872 — permanent repair result != failure-proof transition into permanence:** Intel's hard-PPR power-failure disclosure supplies a bounded example where persistent fuse-programming state can be damaged if power fails during repair. (`H/P`, `E`)
- **1873 — Intel fuse-programming hazard != universal hPPR implementation law:** the patent's partially-blown-fuse failure mode is implementation/problem evidence and must not be projected onto every DDR4 vendor/device. (`H/P`, `X`)
- **1874 — spare-row availability != unlimited future repair capacity:** the bounded Micron product exposes finite repair-row resources, so reserved replacement silicon is retention infrastructure with a consumable capacity boundary. (`H/P`, `E`)
- **1875 — repair infrastructure can outlive the payload it governs:** hard repair state may survive power cycles and continue deciding where later volatile row payloads are placed after prior payload charge has vanished. (`E`)
- **1876 — permanent row retirement != secure erasure:** PPR changes future access resolution; the inspected evidence does not establish overwrite, sanitization, or forensic inaccessibility of the retired defective row. (`E`, `X`)
- **1877 — Case 14 SCSI reassignment ~= Case 119 DDR4 PPR only as a designation/substitution analogy:** both can preserve a logical designation across replacement of a defective physical embodiment, but sector mapping and DRAM row/decoder repair are different mechanisms. (`A`, `X`)
- **1878 — Case 04 mapped Flash ~= Case 119 PPR only at logical-identity/physical-embodiment level:** FTL relocation is ongoing erase/program/reclamation management, whereas PPR is sparse defect repair with bounded spare-row resources. (`A`, `X`)
- **1879 — PPR row substitution != DRAM refresh:** a spare row remains volatile DRAM and continues to require the applicable charge-restoration regime; replacing a row does not satisfy the periodic refresh obligation. (`H/P`, `A`, `X`)
- **1880 — 1979 spare-row prior art != proven 1979→DDR4 PPR genealogy:** the older manufacturing/test-time laser-fuse mechanism blocks an origin myth but does not establish direct standards or implementation descent. (`H/P`, `A`, `X`)
- **1881 — server reboot workflow != universal PPR scheduling law:** Lenovo's named ThinkSystem hard-PPR service path is a deployment witness, not proof that every platform requires reboot-time repair. (`H/P`, `X`)
- **1882 — manufacturer-authored mirror extraction != official archival facsimile:** the bounded Micron semantics are manufacturer text, but the currently inspectable copies are public mirrors; exact official-host provenance remains evidence debt rather than being silently upgraded. (`H/P`, `X`)
- **1883 — related-repository boundary:** current `tmzncty/computing-archaeology` searches for `Post Package Repair` and `PPR DDR4` found no dedicated case; broad semiconductor-redundancy/fuse/JEDEC genealogy belongs there if developed, while Case 119 keeps the retention-specific substitution/lifetime relation. (`H/P` project-state record)
'''.rstrip()
    index = index.rstrip() + findings + "\n"

roadmap_path.write_text(roadmap, encoding="utf-8")
index_path.write_text(index, encoding="utf-8")

# Bounded validation.
for path in (roadmap_path, index_path, case_path, evidence_path):
    text = path.read_text(encoding="utf-8")
    if "\r\n" in text:
        raise SystemExit(f"CRLF unexpectedly present: {path.relative_to(ROOT)}")

if roadmap.count("cases/119-ddr4-post-package-repair-row-remapping.md") != 2:
    raise SystemExit("unexpected Case 119 path count in ROADMAP")
if index.count("cases/119-ddr4-post-package-repair-row-remapping.md") != 1:
    raise SystemExit("unexpected Case 119 path count in CASE_INDEX")
if index.count("## Case 119 — DDR4 Post-Package Repair findings") != 1:
    raise SystemExit("Case 119 findings heading missing or duplicated")
for n in range(1864, 1884):
    if index.count(f"- **{n} —") != 1:
        raise SystemExit(f"finding {n} missing or duplicated")

print("Case 119 navigation/findings integration prepared successfully")
