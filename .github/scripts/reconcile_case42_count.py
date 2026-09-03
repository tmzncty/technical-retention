from pathlib import Path

p = Path('CASE_INDEX.md')
text = p.read_text()
old = '- [x] at least four contrasting cases at `grounded` or better — currently forty-one;'
new = '- [x] at least four contrasting cases at `grounded` or better — currently forty-three;'
if text.count(old) != 1:
    raise SystemExit(f'expected one stale synthesis-gate count, found {text.count(old)}')
text = text.replace(old, new, 1)
if 'currently forty-one;' in text:
    raise SystemExit('stale forty-one synthesis count remains')
p.write_text(text)
print('CASE_INDEX synthesis gate count reconciled to forty-three')
