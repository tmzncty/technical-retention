#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
git pull --ff-only origin main
python3 - <<'PY'
from pathlib import Path
paths = [
    Path('cases/44-nvme13-deallocate-sanitize-forgetting.md'),
    Path('evidence/44-nvme-2011-2017-write-zeroes-value-semantics-deepening.md'),
]
changed = 0
for p in paths:
    s = p.read_text(encoding='utf-8')
    n = s.count('sanitation')
    if n:
        s = s.replace('sanitation', 'sanitization')
        p.write_text(s, encoding='utf-8')
        changed += n
if changed != 2:
    raise SystemExit(f'expected exactly 2 sanitation occurrences, found {changed}')
PY
rm -f .github/workflows/fix-case44-sanitization-term.yml scripts/fix_case44_sanitization_term.sh
git add -A
git commit -m "case44: normalize sanitization terminology"
git push origin main
