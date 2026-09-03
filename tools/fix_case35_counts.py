from pathlib import Path

p = Path('CASE_INDEX.md')
t = p.read_text()
old = "After thirty-three bounded cases, **all thirty-three cases are now `grounded`.**"
new = "After thirty-six bounded cases, **all thirty-six cases are now `grounded`.**"
if old in t:
    t = t.replace(old, new, 1)
elif new not in t:
    raise RuntimeError('cross-case count anchor not found')

old80 = "and temperature-conditioned DRAM-refresh bridges; future write-back-cache, filesystem, refresh, virtual-memory, and distributed regimes"
new80 = "temperature-conditioned DRAM-refresh, and commercial Mobile-DDR automatic-TCSR/selective-retention bridges; future write-back-cache, filesystem, refresh, virtual-memory, and distributed regimes"
if old80 in t:
    t = t.replace(old80, new80, 1)
elif new80 not in t:
    raise RuntimeError('finding-80 mechanism-list anchor not found')

# Keep any synthesis-gate total in sync if it still carries an older count.
t = t.replace('currently thirty-five;', 'currently thirty-six;', 1)
t = t.replace('currently thirty-four;', 'currently thirty-six;', 1)

p.write_text(t)
