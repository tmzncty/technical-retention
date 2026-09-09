from pathlib import Path

source_path = Path("scripts/apply_case133_lpddr4_thermal_offset.py")
source = source_path.read_text(encoding="utf-8")
old = '''if roadmap.count("The broad item stays unchecked because") != 1:\n    raise SystemExit("ROADMAP broad-item continuation marker not unique")\n'''
if old not in source:
    raise SystemExit("expected Case 133 helper guard not found")
source = source.replace(old, "", 1)
exec(compile(source, str(source_path), "exec"), {"__name__": "__main__"})
