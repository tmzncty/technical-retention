#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
git pull --ff-only origin main
python3 - <<'PY'
from pathlib import Path
paths = [
    Path('cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md'),
    Path('evidence/153-ceph-2013-snaptrim-asynchronous-reclamation-grounding.md'),
]
old = 'https://docs.ceph.com/en/nautilus/rados/operations/pg-states/'
new = 'https://docs.ceph.com/en/latest/rados/operations/pg-states/'
for p in paths:
    s = p.read_text(encoding='utf-8')
    if s.count(old) != 1:
        raise SystemExit(f'{p}: expected exactly one old PG-state URL, saw {s.count(old)}')
    p.write_text(s.replace(old, new), encoding='utf-8')
PY
rm -f .github/workflows/fix-case153-pg-states.yml scripts/fix_case153_pg_states.sh
git add -A
git diff --cached --check
git commit -m "case153: use current Ceph PG-state source"
git push origin HEAD:main
