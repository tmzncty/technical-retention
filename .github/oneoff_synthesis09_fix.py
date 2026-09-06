from pathlib import Path

p = Path('docs/SYNTHESIS_09_DISTRIBUTED_CODED_SERVICE_REPAIR_PLACEMENT.md')
text = p.read_text(encoding='utf-8')
old = "successful on-demand reconstruction\n    ==\ndurable fragment replacement"
new = "successful on-demand reconstruction\n    ≠\ndurable fragment replacement"
assert text.count(old) == 1, text.count(old)
p.write_text(text.replace(old, new, 1), encoding='utf-8')
