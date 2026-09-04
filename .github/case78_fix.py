from pathlib import Path
import ast

# Recover the already-staged research payload without executing the first integrator.
staged = Path('.github/case78_integrate.py').read_text()
tree = ast.parse(staged)
vals = {}
for node in tree.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        name = node.targets[0].id
        if name in {'CASE', 'EVIDENCE', 'CASE78_ROW', 'MATRIX78', 'NEW_FINDINGS'}:
            vals[name] = ast.literal_eval(node.value)
for required in {'CASE', 'EVIDENCE', 'CASE78_ROW', 'MATRIX78', 'NEW_FINDINGS'}:
    if required not in vals:
        raise SystemExit(f'missing staged constant {required}')

case_path = Path('cases/78-micron-nand-bad-block-marker-management.md')
evidence_path = Path('evidence/78-micron-2006-2011-nand-bad-block-grounding.md')
if case_path.exists() or evidence_path.exists():
    raise SystemExit('Case 78 payload already exists; refusing duplicate')
case_path.write_text(vals['CASE'])
evidence_path.write_text(vals['EVIDENCE'])

# README: insert directly after Case 77 repository-map entry.
p = Path('README.md')
lines = p.read_text().splitlines()
if not any('cases/78-micron-nand-bad-block-marker-management.md' in x for x in lines):
    hits = [i for i, x in enumerate(lines) if 'cases/77-data-general-dram-sniff-refresh-ecc-scrub.md' in x and x.startswith('- ')]
    if len(hits) != 1:
        raise SystemExit(f'README Case77 anchor count={len(hits)}')
    add = "- [`Case 78 — Micron NAND Bad Blocks: Erasable Factory Defect Marks, Retained Bad-Block Tables, and Replacement`](cases/78-micron-nand-bad-block-marker-management.md) — `grounded`; ONFI 1.0 plus Micron 2009/2011 primary documentation show that factory defect evidence must be captured before destructive erase/program use because the marker itself may be lost, then materialized as a durable bad-block table that is reloaded at reboot and extended when lifetime PROGRAM/ERASE failures force physical replacement. Grounding: [`evidence/78-micron-2006-2011-nand-bad-block-grounding.md`](evidence/78-micron-2006-2011-nand-bad-block-grounding.md)."
    lines.insert(hits[0] + 1, add)
p.write_text('\n'.join(lines) + '\n')

# CASE_INDEX: line-oriented insertion avoids depending on huge surrounding sections.
p = Path('CASE_INDEX.md')
lines = p.read_text().splitlines()
if not any('cases/78-micron-nand-bad-block-marker-management.md' in x for x in lines):
    hits = [i for i, x in enumerate(lines) if x.startswith('| [Data General Dynamic-RAM “Sniffing”')]
    if len(hits) != 1:
        raise SystemExit(f'CASE_INDEX Case77 ledger anchor count={len(hits)}')
    lines.insert(hits[0] + 1, vals['CASE78_ROW'])
if not any(x.startswith('| ONFI/Micron NAND bad-block management / 2006–2011 bounded regime |') for x in lines):
    hits = [i for i, x in enumerate(lines) if x.startswith('| Data General DRAM sniffing / 1980–1983 bounded design |')]
    if len(hits) != 1:
        raise SystemExit(f'CASE_INDEX matrix Case77 anchor count={len(hits)}')
    lines.insert(hits[0] + 1, vals['MATRIX78'])
for i, x in enumerate(lines):
    if x == 'After seventy-eight bounded cases, **all seventy-eight cases are now `grounded`.** The repository satisfies both the numeric and mechanism-variety gates for bounded synthesis. This does **not** make the provisional theses conclusions: new technical bridges must remain free to break or revise the current relational criterion.':
        lines[i] = 'After seventy-nine bounded cases, **all seventy-nine cases are now `grounded`.** The repository satisfies both the numeric and mechanism-variety gates for bounded synthesis. This does **not** make the provisional theses conclusions: new technical bridges must remain free to break or revise the current relational criterion.'
        break
else:
    raise SystemExit('CASE_INDEX aggregate anchor missing')
if not any(x.startswith('925. **physical block survival') for x in lines):
    hits = [i for i, x in enumerate(lines) if x.startswith('924. **Data General 1980 refresh-coupled correction')]
    if len(hits) != 1:
        raise SystemExit(f'finding 924 anchor count={len(hits)}')
    # NEW_FINDINGS begins with the existing 924 line; append only 925+.
    new_lines = vals['NEW_FINDINGS'].splitlines()[1:]
    lines[hits[0] + 1:hits[0] + 1] = new_lines
p.write_text('\n'.join(lines) + '\n')

# ROADMAP: mutate only the SSD/FTL long bullet.
p = Path('ROADMAP.md')
lines = p.read_text().splitlines()
hits = [i for i, x in enumerate(lines) if x.startswith('- [ ] SSD FTL/controller-mediated persistence beyond the bounded Ban/1990s case')]
if len(hits) != 1:
    raise SystemExit(f'ROADMAP SSD bullet anchor count={len(hits)}')
i = hits[0]
line = lines[i]
if 'Cases 15, 20, 30, 31, 32, 36, 37, 38, 39, 44, 47, 52, 55, 59, 65, 66, 67, and 76**' not in line:
    raise SystemExit('ROADMAP case-list phrase missing')
line = line.replace('Cases 15, 20, 30, 31, 32, 36, 37, 38, 39, 44, 47, 52, 55, 59, 65, 66, 67, and 76**', 'Cases 15, 20, 30, 31, 32, 36, 37, 38, 39, 44, 47, 52, 55, 59, 65, 66, 67, 76, and 78**', 1)
if 'cases/78-micron-nand-bad-block-marker-management.md' not in line:
    marker = ' The broad item stays unchecked because '
    if marker not in line:
        raise SystemExit('ROADMAP broad-item boundary missing')
    desc = " [`cases/78-micron-nand-bad-block-marker-management.md`](cases/78-micron-nand-bad-block-marker-management.md), grounded by [`evidence/78-micron-2006-2011-nand-bad-block-grounding.md`](evidence/78-micron-2006-2011-nand-bad-block-grounding.md), adds the factory/runtime bad-block qualification layer: ONFI 1.0 and Micron primary documentation require factory defect marks to be captured before destructive erase/program use, materialized into a BBT that can survive in a good block and be reloaded at reboot, and extended when later PROGRAM/ERASE failures trigger remap/copy into reserved good blocks. This separates physical block survival, defect evidence, allocation authority, logical-address continuity, replacement reserve, garbage collection, wear leveling, and sanitization."
    line = line.replace(marker, desc + marker, 1)
lines[i] = line
p.write_text('\n'.join(lines) + '\n')

# Final validation.
readme = Path('README.md').read_text()
roadmap = Path('ROADMAP.md').read_text()
index = Path('CASE_INDEX.md').read_text()
assert readme.count('cases/78-micron-nand-bad-block-marker-management.md') == 1
assert roadmap.count('cases/78-micron-nand-bad-block-marker-management.md') == 1
assert index.count('cases/78-micron-nand-bad-block-marker-management.md') == 1
assert 'After seventy-nine bounded cases, **all seventy-nine cases are now `grounded`.**' in index
for n in range(925, 941):
    assert f'{n}. **' in index
assert '941. **' not in index
assert Path('cases/78-micron-nand-bad-block-marker-management.md').stat().st_size > 8000
assert Path('evidence/78-micron-2006-2011-nand-bad-block-grounding.md').stat().st_size > 5000

# Clean all one-shot integration machinery from the final tree.
for temp in [
    '.github/case78_integrate.py',
    '.github/case78_fix.py',
    '.github/workflows/case78-integration.yml',
    '.github/workflows/case78-fix-integration.yml',
]:
    Path(temp).unlink(missing_ok=True)
