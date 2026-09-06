from pathlib import Path

path = Path('evidence/55-nvme10-13-smart-health-endurance-grounding.md')
text = path.read_text(encoding='utf-8')
old = '**§7.31.5, SMART READ ATTRIBUTE VALUES, printed p. 93; §7.31.6, SMART RETURN STATUS, printed p. 95; §7.31.7, SMART SAVE ATTRIBUTE VALUES, printed pp. 95–96.**'
new = '**§7.31.5, SMART READ ATTRIBUTE VALUES, printed pp. 91–93 (save-before-return description on p. 92); §7.31.6, SMART RETURN STATUS, printed pp. 94–95; §7.31.7, SMART SAVE ATTRIBUTE VALUES, printed pp. 95–96.**'
if text.count(old) != 1:
    raise RuntimeError(f'expected one locator anchor, found {text.count(old)}')
path.write_text(text.replace(old, new, 1).rstrip() + '\n', encoding='utf-8')
