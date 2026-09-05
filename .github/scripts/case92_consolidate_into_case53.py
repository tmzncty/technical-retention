from pathlib import Path

CASE53 = Path('cases/53-dram-rowhammer-targeted-refresh-policy.md')
EVID53 = Path('evidence/53-rowhammer-2012-2020-targeted-refresh-grounding.md')
CASE92 = Path('cases/92-dram-rowhammer-access-induced-retention-failure.md')
EVID92 = Path('evidence/92-dram-2012-2014-rowhammer-grounding.md')


def insert_before(text: str, marker: str, block: str) -> str:
    if block.strip() in text:
        return text
    idx = text.find(marker)
    if idx < 0:
        raise RuntimeError(f'marker not found: {marker}')
    return text[:idx].rstrip() + '\n\n' + block.strip() + '\n\n' + text[idx:]


def drop_lines_containing(text: str, needles) -> str:
    out = []
    for line in text.splitlines():
        if any(n in line for n in needles):
            continue
        out.append(line)
    return '\n'.join(out) + ('\n' if text.endswith('\n') else '')


# 1) Deepen the already-established Case 53 with the non-duplicative exact anchors
# recovered in the later duplicate Case 92 research pass.
case53 = CASE53.read_text()
case53_block = r'''
### Additional 2014 retention anchors recovered during duplicate-case audit

The later duplicate RowHammer pass recovered three exact ISCA 2014 anchors that strengthen this already-established case and are retained here rather than as a second case number.

First, Kim et al. explicitly distinguish disturbance `victim cells` from ordinary short-retention `weak cells`. In §7 (`Victim Cells ≠ Weak Cells`), they compare RowHammer victims with cells found by a long no-access/no-refresh retention test and report only a small overlap in the characterized modules. The paper cautiously concludes that the coupling pathway responsible for disturbance errors may be independent of the process variation responsible for ordinary weak cells. Therefore **RowHammer victim ≠ merely the shortest ordinary-retention cell** in the bounded experimental record.

Second, the ordinary DRAM access path sharpens the interference relation. Activating a row senses and restores that opened row's charge. Repeated activation can therefore repeatedly restore the aggressor while, through disturbance coupling, accelerating charge loss in nearby victims. The same access episode can be **restorative for one retained state and destructive to another**. This is an engineering reconstruction from the paper's ordinary sense/restore description plus its aggressor/victim measurements, not period terminology.

Third, §8.1 gives a quantitative cost witness for replacing targeted mitigation with globally faster refresh. For the paper's illustrative 8.2 ms refresh interval, estimated refresh-time overhead rises to about 11–35%, compared with the cited 1.4–4.5% baseline range. The numbers are paper/model/sample-specific, but they support the stronger distinction **global faster refresh ≠ targeted refresh**: the former spends maintenance work across the entire array, while the latter requires some access/topology-conditioned selection relation.

These anchors do not change the prior-art boundary already established here: Intel's 2012-priority filing remains the earlier industry witness for row-hammer-specific targeted refresh, and the 2014 paper remains the open experimental characterization / PARA source rather than the origin of the entire engineering problem.
'''
case53 = insert_before(case53, '## Relation to other DRAM cases', case53_block)
CASE53.write_text(case53)

evid53 = EVID53.read_text()
evid53_block = r'''
## B.1 Additional exact ISCA 2014 anchors retained after duplicate-case consolidation

A later research pass accidentally created a second RowHammer case around the same 2012 Intel patent and 2014 Kim et al. paper. That duplicate case has been removed; the useful non-duplicative source anchors are retained here.

### §2.2–§2.4 — aggressor restoration can coexist with victim degradation

Kim et al. describe ordinary row activation as sensing through the row buffer followed by restoration of the opened row's cell charge. Combined with the measured aggressor/victim disturbance relation, this supports the bounded engineering reconstruction:

> repeated aggressor activation can repeatedly restore the aggressor row while contributing to accelerated leakage in physically nearby victim rows.

This is not a claim that the paper used the phrase `aggressor restoration`; it is a mechanism-level inference from the documented access/restore path and disturbance measurements.

### §7 — victim cells are not merely ordinary weak-retention cells

The paper's `Victim Cells ≠ Weak Cells` subsection compares disturbance victims with cells identified by a long no-access/no-refresh retention test and reports little overlap in the characterized modules. The authors state cautiously that the disturbance coupling pathway may be independent of the process variation responsible for ordinary weak cells.

Use this to block:

- `RowHammer victim = shortest ordinary retention-time cell`;
- `RowHammer is only ordinary passive leakage with a uniformly faster clock`.

The conclusion remains sample-bounded to the measured devices.

### §8.1 — quantitative global-refresh cost witness

Kim et al. report that globally shortening the refresh interval can eliminate disturbance errors under the tested conditions, but at substantial performance/energy cost. Their illustrative 8.2 ms interval is associated with estimated refresh-time overhead of roughly 11–35%, compared with the cited baseline range of roughly 1.4–4.5%.

Use this to support:

- `global faster refresh ≠ targeted refresh`;
- the choice of mitigation changes trigger, scope, retained control state, and maintenance cost even when the underlying restoration operation is still refresh.

Do not universalize these percentages beyond the paper's assumptions and devices.
'''
evid53 = insert_before(evid53, '## C. Micron DDR4 `Target Row Refresh Mode` record', evid53_block)
EVID53.write_text(evid53)

# 2) Remove navigation entries that made the duplicate a distinct bounded case.
for filename in ['README.md', 'ROADMAP.md', 'CASE_INDEX.md']:
    p = Path(filename)
    text = p.read_text()
    text = drop_lines_containing(text, [
        'cases/92-dram-rowhammer-access-induced-retention-failure.md',
        'evidence/92-dram-2012-2014-rowhammer-grounding.md',
    ])
    p.write_text(text)

# 3) Repair the roadmap/current-status language to point to the earlier grounded RowHammer case.
p = Path('ROADMAP.md')
text = p.read_text()
text = text.replace(
    '- [ ] refresh failure — **partially advanced by grounded Cases 92 and 93**:',
    '- [ ] refresh failure — **partially advanced by grounded Cases 53 and 93**:',
)
text = text.replace('Case 92 shows that the ordinary recurring refresh schedule', 'Case 53 shows that the ordinary recurring refresh schedule')
text = text.replace('grounded Case 92', 'grounded Case 53')
p.write_text(text)

# 4) Repair later VRT cross-references that had pointed at the duplicate number.
for filename in [
    'cases/93-dram-variable-retention-time-profile-staleness.md',
    'evidence/93-dram-1987-2013-vrt-profiling-grounding.md',
]:
    p = Path(filename)
    text = p.read_text()
    text = text.replace('Case 92', 'Case 53')
    p.write_text(text)

# 5) Keep the useful findings but attribute them to Case 53 deepening instead of a duplicate case.
p = Path('CASE_INDEX.md')
text = p.read_text()
text = text.replace(
    '### Case 92 — DRAM RowHammer findings',
    '### Case 53 deepening — DRAM RowHammer findings consolidated from duplicate Case 92',
)
text = text.replace('Case 92 shows that the ordinary recurring refresh schedule', 'Case 53 shows that the ordinary recurring refresh schedule')
text = text.replace('Cases 92 and 93', 'Cases 53 and 93')
text = text.replace('grounded Case 92', 'grounded Case 53')
text = text.replace(
    'After ninety-four bounded cases, **all ninety-four cases are now `grounded`.**',
    'After ninety-three bounded cases, **all ninety-three cases are now `grounded`.**',
)
p.write_text(text)

# 6) Remove the duplicate case/evidence files. Git history retains them for auditability.
CASE92.unlink()
EVID92.unlink()

# 7) Validate that the canonical case is deepened, duplicate navigation is gone, and the later VRT case now points to Case 53.
assert 'Victim Cells ≠ Weak Cells' in CASE53.read_text()
assert 'B.1 Additional exact ISCA 2014 anchors' in EVID53.read_text()
for filename in ['README.md', 'ROADMAP.md', 'CASE_INDEX.md', 'cases/93-dram-variable-retention-time-profile-staleness.md', 'evidence/93-dram-1987-2013-vrt-profiling-grounding.md']:
    t = Path(filename).read_text()
    if 'cases/92-dram-rowhammer-access-induced-retention-failure.md' in t or 'evidence/92-dram-2012-2014-rowhammer-grounding.md' in t:
        raise RuntimeError(f'duplicate navigation remains in {filename}')
if 'After ninety-three bounded cases, **all ninety-three cases are now `grounded`.**' not in Path('CASE_INDEX.md').read_text():
    raise RuntimeError('aggregate count not repaired')
if 'Cases 53 and 93' not in Path('ROADMAP.md').read_text():
    raise RuntimeError('refresh-failure roadmap cross-reference not repaired')
if 'Case 53' not in Path('cases/93-dram-variable-retention-time-profile-staleness.md').read_text():
    raise RuntimeError('Case 93 RowHammer comparison not redirected to Case 53')

# one-shot integration machinery removes itself
Path('.github/scripts/case92_consolidate_into_case53.py').unlink(missing_ok=True)
Path('.github/workflows/case92-consolidation.yml').unlink(missing_ok=True)
