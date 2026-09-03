from pathlib import Path

p = Path("CASE_INDEX.md")
text = p.read_text(encoding="utf-8")
old = "- [x] at least four contrasting cases at `grounded` or better — currently thirty-seven;"
new = "- [x] at least four contrasting cases at `grounded` or better — currently forty-one;"
if old not in text:
    if new in text:
        raise SystemExit("already fixed")
    raise SystemExit("expected synthesis-count marker not found")
text = text.replace(old, new, 1)
p.write_text(text, encoding="utf-8")
