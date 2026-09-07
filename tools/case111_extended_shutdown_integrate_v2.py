from pathlib import Path
import re

p = Path('tools/case111_extended_shutdown_integrate.py')
source = p.read_text(encoding='utf-8')
old = """nums = [int(m.group(1)) for m in re.finditer(r'^([0-9]+)\\. \\*\\*', index, flags=re.M)]\nif not nums or max(nums) != 1725:\n    raise SystemExit(f'unexpected CASE_INDEX finding max: {max(nums) if nums else None}; expected 1725')"""
new = """nums = [int(m.group(1)) for m in re.finditer(r'^([0-9]+)\\. \\*\\*', index, flags=re.M)]\nnums += [int(m.group(1)) for m in re.finditer(r'^- \\*\\*([0-9]+) —', index, flags=re.M)]\nif not nums or max(nums) != 1725:\n    raise SystemExit(f'unexpected CASE_INDEX finding max: {max(nums) if nums else None}; expected 1725')"""
if old not in source:
    raise SystemExit('expected finding-max block not found in original helper')
source = source.replace(old, new, 1)
# Normalize the new section to the current CASE_INDEX finding style used by 1713–1725.
source = re.sub(r'(?m)^(17(?:2[6-9]|3[0-9]|40))\. \*\*(.*?)\*\* — ', r'- **\1 — \2:** ', source)
source = source.replace("assert '1740. **related-repository boundary**' in INDEX.read_text(encoding='utf-8')", "assert '- **1740 — related-repository boundary:**' in INDEX.read_text(encoding='utf-8')")
exec(compile(source, str(p), 'exec'), {'__name__': '__main__'})
