from pathlib import Path
import ast

staged = Path('.github/case78_integrate.py').read_text()
tree = ast.parse(staged)
vals = {}
for node in tree.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        name = node.targets[0].id
        if name in {'CASE', 'EVIDENCE', 'CASE78_ROW', 'MATRIX78'}:
            vals[name] = ast.literal_eval(node.value)
for required in {'CASE', 'EVIDENCE', 'CASE78_ROW', 'MATRIX78'}:
    if required not in vals:
        raise SystemExit(f'missing staged constant {required}')

case_path = Path('cases/78-micron-nand-bad-block-marker-management.md')
evidence_path = Path('evidence/78-micron-2006-2011-nand-bad-block-grounding.md')
if case_path.exists() or evidence_path.exists():
    raise SystemExit('Case 78 payload already exists; refusing duplicate')
case_path.write_text(vals['CASE'])
evidence_path.write_text(vals['EVIDENCE'])

# README
p = Path('README.md')
lines = p.read_text().splitlines()
hits = [i for i, x in enumerate(lines) if 'cases/77-data-general-dram-sniff-refresh-ecc-scrub.md' in x and x.startswith('- ')]
if len(hits) != 1:
    raise SystemExit(f'README Case77 anchor count={len(hits)}')
lines.insert(hits[0] + 1, "- [`Case 78 — Micron NAND Bad Blocks: Erasable Factory Defect Marks, Retained Bad-Block Tables, and Replacement`](cases/78-micron-nand-bad-block-marker-management.md) — `grounded`; ONFI 1.0 plus Micron 2009/2011 primary documentation show that factory defect evidence must be captured before destructive erase/program use because the marker itself may be lost, then materialized as a durable bad-block table that is reloaded at reboot and extended when lifetime PROGRAM/ERASE failures force physical replacement. Grounding: [`evidence/78-micron-2006-2011-nand-bad-block-grounding.md`](evidence/78-micron-2006-2011-nand-bad-block-grounding.md).")
p.write_text('\n'.join(lines) + '\n')

# CASE_INDEX
p = Path('CASE_INDEX.md')
lines = p.read_text().splitlines()
hits = [i for i, x in enumerate(lines) if x.startswith('| [Data General Dynamic-RAM “Sniffing”')]
if len(hits) != 1:
    raise SystemExit(f'CASE_INDEX ledger anchor count={len(hits)}')
lines.insert(hits[0] + 1, vals['CASE78_ROW'])
hits = [i for i, x in enumerate(lines) if x.startswith('| Data General DRAM sniffing / 1980–1983 bounded design |')]
if len(hits) != 1:
    raise SystemExit(f'CASE_INDEX matrix anchor count={len(hits)}')
lines.insert(hits[0] + 1, vals['MATRIX78'])
agg_old = 'After seventy-eight bounded cases, **all seventy-eight cases are now `grounded`.** The repository satisfies both the numeric and mechanism-variety gates for bounded synthesis. This does **not** make the provisional theses conclusions: new technical bridges must remain free to break or revise the current relational criterion.'
agg_new = 'After seventy-nine bounded cases, **all seventy-nine cases are now `grounded`.** The repository satisfies both the numeric and mechanism-variety gates for bounded synthesis. This does **not** make the provisional theses conclusions: new technical bridges must remain free to break or revise the current relational criterion.'
if lines.count(agg_old) != 1:
    raise SystemExit(f'aggregate anchor count={lines.count(agg_old)}')
lines[lines.index(agg_old)] = agg_new
findings = [
"925. **physical block survival ≠ admissible allocation** — Case 78's factory-marked NAND blocks remain material/addressable objects while retained defect state requires the system to exclude them from normal use;",
"926. **factory defect mark ≠ physical defect** — the marker is evidence created by manufacturing test, not the defect mechanism itself;",
"927. **marker erasure ≠ defect repair** — Micron explicitly warns that bad-block information is erasable and may become unrecoverable after erase, while the reason the block was classified bad need not disappear;",
"928. **defect-evidence retention can require representation change** — the original spare-area mark is scanned into a BBT saved in a good block and then reconstructed as a RAM working table after reboot;",
"929. **durable BBT ≠ RAM working BBT** — one embodiment crosses power loss while the other supports ordinary runtime lookup; loss/recreation boundaries differ even when they represent the same exclusion relation;",
"930. **bad-block table ≠ complete defect history** — the table answers which targets must be excluded/remapped now without preserving all factory test conditions, raw errors, timestamps, or failure chronology;",
"931. **factory bad block ≠ lifetime-developed bad block** — the first arrives with manufacturer-supplied defect evidence; the second can be created by later PROGRAM/ERASE failure status and requires runtime update/replacement;",
"932. **PROGRAM failure ≠ automatic loss of every other page in the block** — Micron's bounded procedure explicitly allows current data from the affected block to be recopied to a replacement;",
"933. **bad-block detection ≠ completed replacement** — identifying a failed physical target creates a new preservation obligation; current payload/correspondence must still be transferred and the exclusion/remap state retained;",
"934. **bad-block replacement ≠ garbage collection** — both can move Flash payload, but Case 78 is triggered by media qualification/failure while Case 04 reclamation is driven by erase/reuse geometry;",
"935. **bad-block replacement ≠ wear leveling** — failure exclusion preserves reliable service; wear leveling distributes physical cycling burden. Micron lists the functions separately;",
"936. **reserved good blocks ≠ simply unused capacity** — withheld physical capacity can be retention infrastructure that permits logical identity to continue after physical-block retirement;",
"937. **logical-address continuity can depend on negative metadata** — a positive map is insufficient when another retained relation must veto known-bad physical targets and redirect access;",
"938. **bad-block retirement ≠ secure sanitization** — exclusion from future allocation does not establish erasure of payload remnants in the retired block;",
"939. **NAND bad-block exclusion ≈ tombstone/revoke only as functional analogy** — each can make a physically surviving candidate inadmissible, but object, scope, lifetime, replication, and mechanism differ;",
"940. **NAND bad-block replacement ≈ SCSI grown-defect reassignment only at the continuity relation** — both can preserve higher-level designation while replacing a physical target, but NAND factory markers/pre-use BBT capture and Flash-specific replacement semantics are not a disk genealogy claim.",
]
hits = [i for i, x in enumerate(lines) if x.startswith('924. **Data General 1980 refresh-coupled correction')]
if len(hits) != 1:
    raise SystemExit(f'finding 924 anchor count={len(hits)}')
lines[hits[0] + 1:hits[0] + 1] = findings
p.write_text('\n'.join(lines) + '\n')

# ROADMAP
p = Path('ROADMAP.md')
lines = p.read_text().splitlines()
hits = [i for i, x in enumerate(lines) if x.startswith('- [ ] SSD FTL/controller-mediated persistence beyond the bounded Ban/1990s case')]
if len(hits) != 1:
    raise SystemExit(f'ROADMAP SSD bullet anchor count={len(hits)}')
i = hits[0]
line = lines[i]
old_cases = 'Cases 15, 20, 30, 31, 32, 36, 37, 38, 39, 44, 47, 52, 55, 59, 65, 66, 67, and 76**'
new_cases = 'Cases 15, 20, 30, 31, 32, 36, 37, 38, 39, 44, 47, 52, 55, 59, 65, 66, 67, 76, and 78**'
if old_cases not in line:
    raise SystemExit('ROADMAP case-list phrase missing')
line = line.replace(old_cases, new_cases, 1)
marker = ' The broad item stays unchecked because '
if marker not in line:
    raise SystemExit('ROADMAP broad-item boundary missing')
desc = " [`cases/78-micron-nand-bad-block-marker-management.md`](cases/78-micron-nand-bad-block-marker-management.md), grounded by [`evidence/78-micron-2006-2011-nand-bad-block-grounding.md`](evidence/78-micron-2006-2011-nand-bad-block-grounding.md), adds the factory/runtime bad-block qualification layer: ONFI 1.0 and Micron primary documentation require factory defect marks to be captured before destructive erase/program use, materialized into a BBT that can survive in a good block and be reloaded at reboot, and extended when later PROGRAM/ERASE failures trigger remap/copy into reserved good blocks. This separates physical block survival, defect evidence, allocation authority, logical-address continuity, replacement reserve, garbage collection, wear leveling, and sanitization."
line = line.replace(marker, desc + marker, 1)
lines[i] = line
p.write_text('\n'.join(lines) + '\n')

# Validation
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
assert case_path.stat().st_size > 8000
assert evidence_path.stat().st_size > 5000

# Remove all temporary machinery, including failed attempts.
for temp in [
    '.github/case78_integrate.py',
    '.github/case78_fix.py',
    '.github/case78_fix2.py',
    '.github/workflows/case78-integration.yml',
    '.github/workflows/case78-fix-integration.yml',
    '.github/workflows/case78-fix2-integration.yml',
]:
    Path(temp).unlink(missing_ok=True)
