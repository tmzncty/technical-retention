from pathlib import Path

p = Path('evidence/52-cai-2009-2015-nand-read-disturb-grounding.md')
s = p.read_text()
s = s.replace(
    'and what evidence existed by 2009–2015 for controller mitigation and recovery?',
    'and what evidence existed from 2002 through 2015 for mechanism recognition, qualification, controller mitigation, and recovery?',
    1,
)
anchor = '- the 2009-priority controller patent directly establishes pre-2015 terminology and read-count/migration prior art;\n'
insert = (
    '- the 2002-priority Fujitsu filing directly establishes earlier manufacturer-primary NAND `read disturb` vocabulary, mechanism class, and a read-voltage tradeoff without proving invention priority;\n'
    '- the 2008 NASA/JPL qualification report independently establishes contemporary reliability guidance while its explicit no-disturb-failure result blocks universal read-count thresholds;\n'
)
if insert.strip() not in s:
    if anchor not in s:
        raise SystemExit('grounding-decision bullet anchor not found')
    s = s.replace(anchor, insert + anchor, 1)
p.write_text(s)

assert 'what evidence existed from 2002 through 2015' in s
assert '2002-priority Fujitsu filing directly establishes' in s
assert '2008 NASA/JPL qualification report independently establishes' in s
