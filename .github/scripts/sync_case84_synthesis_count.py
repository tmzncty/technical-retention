from pathlib import Path

p = Path('CASE_INDEX.md')
text = p.read_text()
old = '- [x] at least four contrasting cases at `grounded` or better — currently fifty-six;'
new = '- [x] at least four contrasting cases at `grounded` or better — currently eighty-five (Cases 00–84);'
if new not in text:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'expected one stale synthesis-count anchor, got {count}')
    text = text.replace(old, new, 1)
p.write_text(text)
if p.read_text().count(new) != 1:
    raise RuntimeError('synthesis count did not update exactly once')
print('case84 synthesis count synced')
