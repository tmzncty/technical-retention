from pathlib import Path

root = Path('.')
idx_path = root / 'CASE_INDEX.md'
idx = idx_path.read_text()

row = "| Micron NAND IDM/COPYBACK / 2006–2015 bounded regime | nonvolatile source-page charge + temporary cache/page-register image + destination-page charge + external/controller ECC relation + higher-level location/currentness state | internal read→register→program relocation; optional external read/check/ECC correction; later program-status checking; policy-dependent block-management/wear-leveling use | COPYBACK can avoid ordinary host data transfer; explicit output/read path restores an integrity-check/correction opportunity that blind internal movement lacks | source page address → internal register → destination page within device-specific movement constraints; higher layer later resolves current logical data to the destination | physical embodiment deliberately changes while the intended logical page may remain the same; already-present correctable errors can move with it | no complete history; current page image plus integrity/mapping state are retained, while move count/check cadence may become bounded maintenance-control state |"

misplaced = "\n---\n\n" + row + "\n\n## Cross-case findings already supported"
correct = "\n" + row + "\n\n---\n\n## Cross-case findings already supported"
if misplaced in idx:
    idx = idx.replace(misplaced, correct, 1)
elif correct not in idx:
    raise SystemExit('Case 82 comparison-row placement not recognized')

old_status = "After eighty-two bounded cases, **all eighty-two cases are now `grounded`.**"
new_status = "After eighty-three bounded cases, **all eighty-three cases are now `grounded`.**"
if old_status in idx:
    idx = idx.replace(old_status, new_status, 1)
elif new_status not in idx:
    raise SystemExit('aggregate case-status sentence not recognized')

idx_path.write_text(idx)

checks = {
    'README.md': 'cases/82-micron-nand-copyback-ecc-requalification.md',
    'ROADMAP.md': 'evidence/82-micron-2006-2015-nand-copyback-grounding.md',
    'CASE_INDEX.md': '1004. **copyback support ≠ safe unrestricted use across devices/generations**',
    'cases/82-micron-nand-copyback-ecc-requalification.md': '**`grounded`**',
    'evidence/82-micron-2006-2015-nand-copyback-grounding.md': '**Case 82 may be marked `grounded`.**',
}
for path, needle in checks.items():
    data = (root / path).read_text()
    if needle not in data:
        raise SystemExit(f'missing {needle} in {path}')

case_files = sorted((root / 'cases').glob('[0-9][0-9]-*.md'))
nums = sorted(int(f.name[:2]) for f in case_files)
if nums != list(range(83)):
    raise SystemExit(f'case numbering not contiguous 00-82: {nums[-10:]}')

print('case82 corrected integration validation passed')
