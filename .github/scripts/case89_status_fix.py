from pathlib import Path

p = Path('CASE_INDEX.md')
text = p.read_text()
old = 'After ninety bounded cases, **all eighty-nine cases are now `grounded`.**'
new = 'After ninety bounded cases, **all ninety cases are now `grounded`.**'
if old not in text:
    raise RuntimeError('expected Case 89 aggregate-status sentence not found')
if text.count(old) != 1:
    raise RuntimeError('aggregate-status sentence is not unique')
text = text.replace(old, new)
p.write_text(text)
if new not in p.read_text():
    raise RuntimeError('aggregate-status replacement failed')
Path('.github/scripts/case89_status_fix.py').unlink(missing_ok=True)
Path('.github/workflows/case89-status-fix.yml').unlink(missing_ok=True)
