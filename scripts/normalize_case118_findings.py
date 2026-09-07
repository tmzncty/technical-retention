import re
from pathlib import Path

path = Path("CASE_INDEX.md")
text = path.read_text(encoding="utf-8")
heading = "## Case 118 — Micron DDR5 Directed Refresh Management findings"
if heading not in text:
    raise SystemExit("Case 118 findings heading missing")
prefix, section = text.split(heading, 1)
fixed, count = re.subn(r"(?m)^- \*\*(\d+) — \*\*", r"- **\1 — ", section)
if count != 17:
    raise SystemExit(f"expected 17 malformed Case 118 findings, fixed {count}")
text = prefix + heading + fixed
path.write_text(text, encoding="utf-8")
print("Normalized 17 Case 118 finding labels")
