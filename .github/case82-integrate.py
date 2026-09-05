from pathlib import Path
import re

ROOT = Path('.')


def insert_after_line(text: str, needle: str, new_line: str) -> str:
    if new_line in text:
        return text
    lines = text.splitlines()
    hits = [i for i, line in enumerate(lines) if needle in line]
    if not hits:
        raise SystemExit(f'anchor not found: {needle}')
    i = hits[-1]
    lines.insert(i + 1, new_line)
    return '\n'.join(lines) + ('\n' if text.endswith('\n') else '')


# README navigation
p = ROOT / 'README.md'
text = p.read_text()
readme_line = "- [`cases/82-micron-nand-copyback-ecc-requalification.md`](cases/82-micron-nand-copyback-ecc-requalification.md) — grounded NAND internal-relocation integrity bridge: Micron IDM/COPYBACK moves a page through an internal register without ordinary external data transfer, but the same fast path can bypass controller-side ECC correction so inherited errors follow the new physical embodiment; relocation, operation completion, integrity requalification, Correct-and-Refresh, garbage collection, and wear leveling remain separate relations."
text = insert_after_line(text, 'cases/81-chain-replication-tail-currentness-reconfiguration.md', readme_line)
p.write_text(text)

# ROADMAP completed bridge
p = ROOT / 'ROADMAP.md'
text = p.read_text()
roadmap_line = "- [x] NAND internal data move / COPYBACK integrity boundary — [`cases/82-micron-nand-copyback-ecc-requalification.md`](cases/82-micron-nand-copyback-ecc-requalification.md), grounded by [`evidence/82-micron-2006-2015-nand-copyback-grounding.md`](evidence/82-micron-2006-2015-nand-copyback-grounding.md), adds a bounded Micron raw-NAND migration regime in which an internal read→register→program path avoids ordinary external data transfer but can also bypass controller-side ECC correction, so already-present errors can follow the page to its new physical embodiment. Micron's TN-29-15/TN-29-41 and a later named product witness separate relocation from integrity requalification and recommend explicit read/check/correction when error-margin renewal is required. This remains distinct from Case 04 mapping/reclamation, Case 36 Correct-and-Refresh, Cases 52/59 disturbance mechanisms, Case 67 reclaim policy, and Case 78 bad-block retirement; a full cross-vendor/ONFI copyback genealogy belongs in `computing-archaeology`."
text = insert_after_line(text, 'cases/81-chain-replication-tail-currentness-reconfiguration.md', roadmap_line)
p.write_text(text)

# CASE_INDEX ledger, aggregate, matrix, and findings
p = ROOT / 'CASE_INDEX.md'
text = p.read_text()

# Update only pre-existing aggregate wording before adding Case 82 text.
text = text.replace('00–81', '00–82')
text = re.sub(r'\b82 bounded cases\b', '83 bounded cases', text)
text = text.replace('all **82** are `grounded`', 'all **83** are `grounded`')
text = text.replace('**82** are `grounded`', '**83** are `grounded`')
text = text.replace('82 of 82', '83 of 83')

ledger_row = "| [Micron NAND Internal Data Move / COPYBACK: Relocation Without Automatic ECC Requalification](cases/82-micron-nand-copyback-ecc-requalification.md) | **grounded** | raw NAND source page + internal cache/page register + destination page + controller ECC/integrity state + higher-layer relocation/currentness relation | separate physical relocation from integrity requalification; operation completion from content correction; logical identity continuity from remaining ECC margin; and movement primitive from GC/wear-leveling/reclaim policy | [2006–2015 Micron NAND copyback grounding](evidence/82-micron-2006-2015-nand-copyback-grounding.md); official TN-29-41 archival facsimile, cross-vendor/ONFI command genealogy, modern on-die-ECC variants, and independent controller fault validation remain separate work |"
text = insert_after_line(text, 'cases/81-chain-replication-tail-currentness-reconfiguration.md', ledger_row)

matrix_row = "| Micron NAND IDM/COPYBACK / 2006–2015 bounded regime | nonvolatile source-page charge + temporary cache/page-register image + destination-page charge + external/controller ECC relation + higher-level location/currentness state | internal read→register→program relocation; optional external read/check/ECC correction; later program-status checking; policy-dependent block-management/wear-leveling use | COPYBACK can avoid ordinary host data transfer; explicit output/read path restores an integrity-check/correction opportunity that blind internal movement lacks | source page address → internal register → destination page within device-specific movement constraints; higher layer later resolves current logical data to the destination | physical embodiment deliberately changes while the intended logical page may remain the same; already-present correctable errors can move with it | no complete history; current page image plus integrity/mapping state are retained, while move count/check cadence may become bounded maintenance-control state |"
if matrix_row not in text:
    anchor = '\n## Cross-case findings'
    if anchor not in text:
        raise SystemExit('comparison-matrix end anchor not found')
    text = text.replace(anchor, '\n' + matrix_row + '\n' + anchor, 1)

findings = r'''

## Case 82 — Micron NAND internal-data-move / COPYBACK findings

989. **internal relocation ≠ external ECC requalification** — Micron's bounded IDM/COPYBACK path moves a page through an internal register without the ordinary controller-side read/correct/reprogram path;
990. **new physical embodiment ≠ renewed error-free representation** — an already-present source-page bit error can follow the internal read and then be programmed into the destination;
991. **payload identity continuity ≠ raw-bit-pattern cleanliness** — the intended logical page can remain recoverable while its current physical image already consumes some correction margin;
992. **correctable error presence ≠ immediate logical failure** — the bounded failure risk arises when accumulated errors outrun the available correction/recovery path, not merely when the first correctable error exists;
993. **remaining ECC margin can change while logical location service continues** — mapping can successfully point to a new current page even though the page carries forward a larger error population;
994. **page-register transit ≠ durable destination retention** — the internal cache/page register is a temporary embodiment in a source→register→destination handoff, not the intended long-term retained location;
995. **program-operation success ≠ proof of source-content requalification** — device status can establish that COPYBACK PROGRAM completed while Micron separately recommends reading/verifying data to prevent propagation of inherited errors;
996. **bus-avoidance performance work can remove a validation opportunity** — the feature's speed/power advantage comes partly from not sending data through the external path where error correction can otherwise occur;
997. **migration can carry error debt forward as well as value** — physical renewal of location can preserve a correctable imperfection rather than reset the page to the intended error-free representation;
998. **migration primitive ≠ migration policy** — COPYBACK/IDM is a mechanism for moving a page; garbage collection, wear leveling, reclaim, or bad-block replacement are policies/maintenance regimes that may choose whether and when to move data;
999. **COPYBACK ≠ Correct-and-Refresh** — Case 36 deliberately couples read/ECC correction with rewrite/remap to renew retention margin, whereas the bounded blind internal move can skip that correction step;
1000. **COPYBACK ≠ read disturb or program interference** — Cases 52 and 59 explain mechanisms that create physical error shifts; Case 82 only requires the weaker fact that an existing error population can be propagated when correction is bypassed;
1001. **reclaim trigger ≠ relocation integrity path** — Case 67 can decide that a stressed block should be relocated, while Case 82 asks whether the chosen movement path merely copies or also requalifies/corrects the data;
1002. **bad-block exclusion ≠ payload-integrity renewal** — Case 78's decision to retire a block and choose a reserve does not by itself establish whether the copied page was corrected before the replacement became current;
1003. **historical `IDM` / `COPYBACK` vocabulary ≠ invention priority** — Micron documentation grounds the bounded mechanism and terminology but does not establish who first invented internal NAND page movement;
1004. **copyback support ≠ safe unrestricted use across devices/generations** — device-specific movement geometry, ECC placement, verification policy, and later on-die-ECC designs must be sourced separately rather than universalized from the bounded Micron regime.
'''
if '## Case 82 — Micron NAND internal-data-move / COPYBACK findings' not in text:
    text = text.rstrip() + findings + '\n'

p.write_text(text)

# Validation
case_files = sorted((ROOT / 'cases').glob('[0-9][0-9]-*.md'))
nums = sorted(int(f.name[:2]) for f in case_files)
expected = list(range(83))
if nums != expected:
    raise SystemExit(f'case numbering not contiguous 00-82: {nums[-10:]}')

for path, needle in [
    ('README.md', 'cases/82-micron-nand-copyback-ecc-requalification.md'),
    ('ROADMAP.md', 'evidence/82-micron-2006-2015-nand-copyback-grounding.md'),
    ('CASE_INDEX.md', 'cases/82-micron-nand-copyback-ecc-requalification.md'),
    ('CASE_INDEX.md', '## Case 82 — Micron NAND internal-data-move / COPYBACK findings'),
    ('CASE_INDEX.md', '1004. **copyback support ≠ safe unrestricted use across devices/generations**'),
]:
    data = (ROOT / path).read_text()
    if needle not in data:
        raise SystemExit(f'missing {needle} in {path}')

if not (ROOT / 'cases/82-micron-nand-copyback-ecc-requalification.md').exists():
    raise SystemExit('case file missing')
if not (ROOT / 'evidence/82-micron-2006-2015-nand-copyback-grounding.md').exists():
    raise SystemExit('evidence file missing')

print('case82 integration validation passed')
