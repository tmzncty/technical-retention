#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
git pull --ff-only origin main

python3 - <<'PY'
from pathlib import Path
import re

case33 = Path('cases/33-micron-ddr5-same-bank-refresh-localization.md')
case106 = Path('cases/106-ddr5-same-bank-refresh-parallel-target-set.md')
case151 = Path('cases/151-ddr5-same-bank-refresh-partitioned-maintenance.md')
ev151 = Path('evidence/151-ddr5-2014-2020-bank-scoped-refresh-grounding.md')
index = Path('CASE_INDEX.md')
roadmap = Path('ROADMAP.md')

for p in [case33, case106, case151, ev151, index, roadmap,
          Path('cases/105-micron-lpddr2-per-bank-refresh-maintenance-granularity.md'),
          Path('cases/139-lpddr3-lpddr4-per-bank-refresh-target-authority.md')]:
    if not p.exists():
        raise SystemExit(f'missing expected path: {p}')

# 1) Strengthen the surviving DDR5 cases with explicit division of labor so the
# same refresh geometry is not opened as another standalone case later.
insert33 = '''## Coverage consolidation

Case 33 now serves as the **manufacturer-primary service/interference-geometry** entry for DDR5 Same Bank Refresh. It should be read together with, rather than duplicated by:

- [`Case 106`](106-ddr5-same-bank-refresh-parallel-target-set.md), which carries the earlier **December 2017 proposed-spec draft** and the stronger bank-index synchronization / coverage-accounting evidence;
- [`Case 105`](105-micron-lpddr2-per-bank-refresh-maintenance-granularity.md), which grounds the earlier LPDDR2 one-bank `REFpb` product regime and prevents a DDR5 invention-priority reading;
- [`Case 139`](139-lpddr3-lpddr4-per-bank-refresh-target-authority.md), which isolates the LPDDR3→LPDDR4 change in **who selects the next per-bank target**.

These are complementary slices, not an invention ladder. The shared functional relation is that refresh work can be spatially localized while broader retention obligations remain; target geometry, target-selection authority, coverage accounting, and service interference must still be kept distinct.

A later Case 151 repeated these already-grounded relations without adding a new retention axis and has therefore been retired from the active case set instead of being maintained as a separate duplicate.

'''

s = case33.read_text(encoding='utf-8')
if '## Coverage consolidation' not in s:
    marker = '## Functional analogy and philosophical limit\n'
    if s.count(marker) != 1:
        raise SystemExit(f'{case33}: expected one insertion marker, found {s.count(marker)}')
    s = s.replace(marker, insert33 + marker)
    case33.write_text(s, encoding='utf-8')

insert106 = '''## Coverage relationship with Case 33 and LPDDR controls

This case is intentionally narrower than [`Case 33`](33-micron-ddr5-same-bank-refresh-localization.md), not a second independent claim that DDR5 introduced localized refresh. Case 33 carries Micron's 2019–2023 manufacturer-primary evidence for target idleness, lockout, residual timing, and service interference. Case 106 carries the earlier **2017 proposed-spec floor** plus explicit bank-index synchronization and coverage accounting. The two should be cited together when both chronology and operational geometry matter.

Earlier per-bank refresh is already bounded separately in [`Case 105`](105-micron-lpddr2-per-bank-refresh-maintenance-granularity.md), while [`Case 139`](139-lpddr3-lpddr4-per-bank-refresh-target-authority.md) isolates the LPDDR3→LPDDR4 migration of bank-target selection authority. Chronology across these cases is not treated as direct genealogy.

'''

s = case106.read_text(encoding='utf-8')
if '## Coverage relationship with Case 33 and LPDDR controls' not in s:
    marker = '## Functional analogy and philosophical limit\n'
    if s.count(marker) != 1:
        raise SystemExit(f'{case106}: expected one insertion marker, found {s.count(marker)}')
    s = s.replace(marker, insert106 + marker)
    case106.write_text(s, encoding='utf-8')

# 2) Retire the duplicate numbered case and its evidence record.
case151.unlink()
ev151.unlink()

# 3) Repair CASE_INDEX: remove the duplicate findings block, add an explicit
# consolidation note, and restore navigation rows for Cases 152 and 153.
s = index.read_text(encoding='utf-8')
pat = re.compile(r'\n### Case 151 — DDR5 Same Bank Refresh: Partitioned Refresh Scope\n.*?(?=\n### Case 152 —)', re.S)
m = pat.search(s)
if not m:
    raise SystemExit('CASE_INDEX: Case 151 findings block not found')
replacement = '''
### DDR bank-scoped refresh coverage consolidation

The former Case 151 duplicated already-grounded coverage and has been retired. Use Case 33 for DDR5 manufacturer-primary maintenance-interference geometry, Case 106 for the 2017 proposed-spec target-set / coverage-accounting floor, Case 105 for LPDDR2 per-bank refresh, and Case 139 for LPDDR3→LPDDR4 target-selection authority. No numbered findings are retained for the retired duplicate.
'''
s = s[:m.start()] + replacement + s[m.end():]

if 'cases/152-sqlite-wal-checkpoint-backfill-reader-retention.md' not in s:
    marker = '## Comparison matrix — provisional\n'
    if s.count(marker) != 1:
        raise SystemExit(f'CASE_INDEX: expected one comparison-matrix marker, found {s.count(marker)}')
    rows = '''| [SQLite WAL Checkpoint: Committed-but-Unbackfilled State, Reader End Marks, and Reuse Authority](cases/152-sqlite-wal-checkpoint-backfill-reader-retention.md) | **grounded** | committed WAL frames + reader end marks + checkpoint/backfill progress + reader-gated WAL reuse + reconstructible wal-index | distinguish transaction commit from checkpoint; current state from main-file-only state; payload backfill from reuse authority; persistent WAL evidence from transient lookup state | [2010 SQLite grounding + ARIES prior-art guardrail](evidence/152-sqlite-2010-wal-checkpoint-retention-grounding.md); later checkpoint modes, lower-layer durability, WAL2/experimental branches, and media sanitization remain separate |
| [Ceph RADOS Snap Trimming: Snapshot Retirement, Clone Liveness, and Asynchronous Reclamation](cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md) | **grounded** | retired snapshot relation + clone membership/liveness + asynchronous trim queue/work + replica/log/recovery state | distinguish snapshot retirement from clone reclamation; one retired membership from shared-clone disposability; queued/executing/completed cleanup; logical trim from physical sanitization | [2013 source-tree + maintained Ceph grounding](evidence/153-ceph-2013-snaptrim-asynchronous-reclamation-grounding.md); first-introduction genealogy, internal representation transitions, lower-layer allocator timing, and fault injection remain open |
'''
    s = s.replace(marker, rows + marker)

if '### Case 151 —' in s:
    raise SystemExit('CASE_INDEX: duplicate Case 151 heading survived')
index.write_text(s, encoding='utf-8')

# 4) Replace the roadmap's duplicate-case completion line with a durable routing note.
s = roadmap.read_text(encoding='utf-8')
old = '- [x] Ground DDR5 same-bank refresh as a partitioned-maintenance case: JESD79-5 public boundary (2020), Micron `REFsb` one-bank-per-bank-group scope, untargeted-bank service continuity, LPDDR2 per-bank prior-art floor, and strict no-genealogy/no-controller-policy/no-sanitization boundaries (Case 151).'
new = '- [x] **DDR bank-scoped refresh coverage consolidated** — retire duplicate Case 151 and route the established dimensions to Case 33 (Micron 2019–2023 target/service-interference geometry), Case 106 (2017 proposed-spec target-set and coverage accounting), Case 105 (LPDDR2 one-bank `REFpb` prior-art/product floor), and Case 139 (LPDDR3→LPDDR4 bank-target scheduling authority). These are complementary bounded slices, not a direct genealogy.'
if s.count(old) != 1:
    raise SystemExit(f'ROADMAP: expected one Case 151 completion line, found {s.count(old)}')
s = s.replace(old, new)
roadmap.write_text(s, encoding='utf-8')

# 5) Repository-level invariants for this consolidation.
for p in [index, roadmap, case33, case106]:
    text = p.read_text(encoding='utf-8')
    if 'cases/151-ddr5-same-bank-refresh-partitioned-maintenance.md' in text:
        raise SystemExit(f'{p}: stale Case 151 path remains')
    if 'evidence/151-ddr5-2014-2020-bank-scoped-refresh-grounding.md' in text:
        raise SystemExit(f'{p}: stale Evidence 151 path remains')

for linked in [
    Path('cases/33-micron-ddr5-same-bank-refresh-localization.md'),
    Path('cases/105-micron-lpddr2-per-bank-refresh-maintenance-granularity.md'),
    Path('cases/106-ddr5-same-bank-refresh-parallel-target-set.md'),
    Path('cases/139-lpddr3-lpddr4-per-bank-refresh-target-authority.md'),
    Path('cases/152-sqlite-wal-checkpoint-backfill-reader-retention.md'),
    Path('cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md'),
    Path('evidence/152-sqlite-2010-wal-checkpoint-retention-grounding.md'),
    Path('evidence/153-ceph-2013-snaptrim-asynchronous-reclamation-grounding.md'),
]:
    if not linked.exists():
        raise SystemExit(f'expected linked path missing: {linked}')
PY

# No active file should still link to the retired duplicate paths.
if git grep -n 'cases/151-ddr5-same-bank-refresh-partitioned-maintenance.md\|evidence/151-ddr5-2014-2020-bank-scoped-refresh-grounding.md' -- ':!scripts/consolidate_ddr_refresh_coverage.sh'; then
  echo 'stale Case 151 path reference remains' >&2
  exit 1
fi

rm -f .github/workflows/consolidate-ddr-refresh-coverage.yml scripts/consolidate_ddr_refresh_coverage.sh

git add -A
git diff --cached --check

git diff --cached --name-status

git commit -m "dram: consolidate duplicate bank-refresh coverage"
git push origin HEAD:main
