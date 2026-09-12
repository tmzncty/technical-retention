from pathlib import Path

p = Path('CASE_INDEX.md')
text = p.read_text(encoding='utf-8')
assert '- **3555 —' in text
p.write_text(text.rstrip() + '\n', encoding='utf-8')

Path('.github/scripts/tmp_case111_normalize.py').unlink()
Path('.github/workflows/tmp-case111-normalize.yml').unlink()
