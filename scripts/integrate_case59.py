from pathlib import Path
import re

ROOT = Path('.')
readme_p = ROOT / 'README.md'
roadmap_p = ROOT / 'ROADMAP.md'
index_p = ROOT / 'CASE_INDEX.md'

readme = readme_p.read_text(encoding='utf-8')
roadmap = roadmap_p.read_text(encoding='utf-8')
index = index_p.read_text(encoding='utf-8')

case_path = 'cases/59-nand-program-interference-write-induced-neighbor-drift.md'
evidence_path = 'evidence/59-nand-2002-2014-program-interference-grounding.md'

# README navigation: append Case 59 immediately after Case 58.
readme_line = (
    '- [`cases/59-nand-program-interference-write-induced-neighbor-drift.md`]'
    '(cases/59-nand-program-interference-write-induced-neighbor-drift.md) — grounded NAND program-interference bridge: '
    'programming one planar floating-gate MLC NAND cell/page can capacitively shift an already-programmed physical neighbor; '
    'coupling geometry, page-program order, neighbor data, ECC margin, and read-reference interpretation remain separate, while 2002 and 2007–2008 prior art prevent a false 2013 invention claim.\n'
)
if case_path not in readme:
    lines = readme.splitlines(keepends=True)
    out = []
    inserted = False
    for line in lines:
        out.append(line)
        if 'cases/58-raft-snapshot-log-compaction.md' in line:
            out.append(readme_line)
            inserted = True
    if not inserted:
        raise SystemExit('README Case 58 anchor not found')
    readme = ''.join(out)

# ROADMAP: update the SSD/controller bridge list and add one bounded summary.
start = roadmap.find('- [ ] SSD FTL/controller-mediated persistence beyond the bounded Ban/1990s case')
end = roadmap.find('\n- [ ] RAID / scrubbing / rebuild', start)
if start < 0 or end < 0:
    raise SystemExit('ROADMAP SSD block anchors not found')
block = roadmap[start:end]
old_list = 'grounded Cases 15, 20, 30, 31, 32, 36, 37, 38, 39, 44, 47, 52, and 55'
new_list = 'grounded Cases 15, 20, 30, 31, 32, 36, 37, 38, 39, 44, 47, 52, 55, and 59'
if old_list in block:
    block = block.replace(old_list, new_list, 1)
elif new_list not in block:
    raise SystemExit('ROADMAP SSD case-list text not found')
roadmap_sentence = (
    '[`cases/59-nand-program-interference-write-induced-neighbor-drift.md`]'
    '(cases/59-nand-program-interference-write-induced-neighbor-drift.md), grounded by '
    '[`evidence/59-nand-2002-2014-program-interference-grounding.md`]'
    '(evidence/59-nand-2002-2014-program-interference-grounding.md), adds a write-induced neighbor-coupling regime: '
    'an aggressor program operation can shift an already-programmed victim threshold distribution through parasitic capacitance, '
    'and measured reliability depends on physical location, page-program order, and neighbor data; later read-reference adaptation can recover logical interpretation without restoring the pre-interference physical voltage. '
)
if case_path not in block:
    marker = ' The broad item stays unchecked because'
    if marker not in block:
        raise SystemExit('ROADMAP SSD broad-item marker not found')
    block = block.replace(marker, ' ' + roadmap_sentence + marker, 1)
roadmap = roadmap[:start] + block + roadmap[end:]

# CASE_INDEX case ledger row.
case_row = (
    '| [NAND Flash Program Interference: Write-Induced Neighbor Drift, Program Order, and Read-Reference Recovery]'
    '(cases/59-nand-program-interference-write-induced-neighbor-drift.md) | **grounded** | '
    'planar floating-gate MLC NAND + victim/aggressor capacitive coupling + page-program-order history + data-dependent threshold shift + read-reference/ECC recovery | '
    'separate logical write target from physical effect scope; program sequence from elapsed retention age; neighbor coupling from read disturb; and logical recovery by adapted interpretation from restoration of the prior physical threshold state | '
    '[2002–2014 NAND program-interference grounding](evidence/59-nand-2002-2014-program-interference-grounding.md); modern 3D/charge-trap geometry, named-controller deployment, exact vendor program-order contracts, and independent product fault validation remain separate work |\n'
)
if case_path not in index:
    lines = index.splitlines(keepends=True)
    out = []
    inserted = False
    for line in lines:
        out.append(line)
        if 'cases/58-raft-snapshot-log-compaction.md' in line and line.startswith('| ['):
            out.append(case_row)
            inserted = True
    if not inserted:
        raise SystemExit('CASE_INDEX Case 58 row anchor not found')
    index = ''.join(out)

# Comparison matrix row, after the Raft matrix row if present.
matrix_row = (
    '| NAND program interference / 2002–2014 bounded planar-MLC regime | '
    'floating-gate threshold state + physical neighbor-coupling geometry + program-order/data context + read-reference/ECC interpretation | '
    'program-order discipline/device design to reduce later aggressor exposure; controller modeling/read-reference adaptation and ECC can recover shifted states without undoing the shift | '
    'ordinary read interprets a possibly shifted distribution through reference voltages; proposed NAC can reread using neighbor-conditioned references after ECC failure | '
    'logical page/cell designation remains distinct from physical victim/aggressor geometry and conditional neighbor state | '
    'fixed physical cells in the bounded experiment, but retained margin is relational to later neighboring programs; higher-level FTL relocation remains a separate mechanism | '
    'no complete history; current payload plus enough program-order/neighbor/model policy context may influence later reliable recovery |\n'
)
if '| NAND program interference / 2002–2014 bounded planar-MLC regime |' not in index:
    mstart = index.find('## Comparison matrix')
    mend = index.find('\n## ', mstart + len('## Comparison matrix'))
    if mstart < 0:
        raise SystemExit('comparison matrix heading not found')
    if mend < 0:
        mend = len(index)
    segment = index[mstart:mend]
    seg_lines = segment.splitlines(keepends=True)
    pos = None
    for i, line in enumerate(seg_lines):
        if line.startswith('|') and 'Raft' in line and ('snapshot' in line.lower() or 'Snapshot' in line):
            pos = i + 1
    if pos is None:
        # Fall back to inserting after the last table row in the matrix section.
        table_positions = [i for i, line in enumerate(seg_lines) if line.startswith('|')]
        if not table_positions:
            raise SystemExit('comparison matrix table not found')
        pos = table_positions[-1] + 1
    seg_lines.insert(pos, matrix_row)
    index = index[:mstart] + ''.join(seg_lines) + index[mend:]

# Case 59 cross-case findings. Keep the numbered ledger monotonic.
findings = '''\n\n## Case 59 — NAND program-interference findings\n\n621. **Successful aggressor programming ≠ unchanged neighboring retained state.** In the bounded planar MLC regime, programming a neighboring floating gate can capacitively shift an already-programmed victim threshold distribution even though the victim was not the write target.\n622. **Logical write target ≠ complete physical electrical-effect scope.** Host/page selection names the intended update, while parasitic coupling determines a wider physical side-effect geometry.\n623. **Logical page independence ≠ physical retention independence.** Two pages can be separately addressable while the reliability margin of one depends on later programming of a physical neighbor.\n624. **Program-order history can matter even when elapsed retention age is held aside.** The 2013 tests show materially different victim interference under in-page-order and tested out-of-page-order programming.\n625. **Same final set of programmed pages ≠ necessarily the same interference history.** Which neighboring LSB/MSB transitions occur after the victim can change how many interference events it receives; this remains bounded to the measured two-bit MLC regime.\n626. **Neighbor data value can affect victim retention margin without becoming victim payload.** Larger aggressor threshold transitions can induce larger coupled victim shifts, so physical recoverability is relational without redefining logical identity.\n627. **Physical adjacency/coupling geometry ≠ logical namespace adjacency.** Wordline/direct-neighbor relations dominate the bounded measurements; controller-visible logical designations alone do not describe the electrical coupling relation.\n628. **Program interference ≠ retention-age leakage.** Cai et al. explicitly separate neighbor-program-induced errors from gradual retention charge loss even though both consume raw-error/ECC margin.\n629. **Program interference ≠ read disturb.** Case 52 accumulates pass-voltage stress through reads; Case 59 couples an aggressor programming transition into a victim. Shared cross-target side effects do not imply one mechanism or maintenance clock.\n630. **Cell-to-cell program interference ≠ every use of `program disturb`.** Related NAND literature uses program-disturb vocabulary for other inhibited/unselected-cell program-path failures; mechanism must be checked before terminology is merged.\n631. **Read-reference recovery ≠ physical-state restoration.** Adjusting the discrimination voltage can recover the intended logical value from a shifted victim distribution without returning the floating-gate threshold to its pre-interference position.\n632. **Recovery criterion can adapt to medium history.** The 2013 controller proposal learns/predicts post-interference distributions and changes later read boundaries; reliable continuation can therefore depend on interpretation policy as well as the retained charge state.\n633. **Neighbor retained state can become decoding side information.** The 2014 NAC proposal conditions reread references on immediate-neighbor values after ECC failure, using another retained value to improve recovery of the victim.\n634. **Research mitigation evaluation ≠ named-controller deployment.** The 2013 dynamic-reference and 2014 NAC results are experimental/model/simulation evidence and must not be upgraded into claims about shipped SSD firmware.\n635. **2013 commercial-chip characterization ≠ invention of NAND cell-to-cell interference or program-order mitigation.** Lee et al. document floating-gate interference in 2002, and Samsung-linked 2007–2008 work already treats cell-to-cell coupling/program architecture/order as a mitigation problem.\n'''
if '## Case 59 — NAND program-interference findings' not in index:
    anchor = '620. **Raft 2014 snapshotting ≠ invention of snapshotting/log compaction.**'
    p = index.find(anchor)
    if p < 0:
        raise SystemExit('Case 58 finding 620 anchor not found')
    line_end = index.find('\n', p)
    if line_end < 0:
        line_end = len(index)
    index = index[:line_end] + findings + index[line_end:]

# Conservative count wording updates, if any current summary uses them.
for old, new in [
    ('59 bounded cases', '60 bounded cases'),
    ('59 grounded cases', '60 grounded cases'),
    ('fifty-nine bounded cases', 'sixty bounded cases'),
    ('fifty-nine grounded cases', 'sixty grounded cases'),
]:
    index = index.replace(old, new)
    readme = readme.replace(old, new)
    roadmap = roadmap.replace(old, new)

# Validate navigation and ledger before writing.
case_table = index.split('## Cases', 1)[1].split('\n---\n', 1)[0]
paths = re.findall(r'\(cases/(\d{2})-[^)]+\.md\)', case_table)
if len(paths) != 60 or len(set(paths)) != 60 or set(paths) != {f'{i:02d}' for i in range(60)}:
    raise SystemExit(f'case ledger validation failed: count={len(paths)} unique={len(set(paths))} tail={paths[-5:]}')
if case_table.count('**grounded**') != 60:
    raise SystemExit(f'grounded case count validation failed: {case_table.count("**grounded**")}')
for name, text in [('README', readme), ('ROADMAP', roadmap), ('CASE_INDEX', index)]:
    if text.count(case_path) != (1 if name != 'CASE_INDEX' else 1):
        # CASE_INDEX also links the evidence separately, but the case path itself should occur once in the case row.
        raise SystemExit(f'{name} case path count unexpected: {text.count(case_path)}')
if index.count(evidence_path) != 1:
    raise SystemExit(f'CASE_INDEX evidence path count unexpected: {index.count(evidence_path)}')
if index.count('## Case 59 — NAND program-interference findings') != 1:
    raise SystemExit('Case 59 findings missing/duplicated')
if index.count('621. **Successful aggressor programming') != 1 or index.count('635. **2013 commercial-chip characterization') != 1:
    raise SystemExit('Case 59 numbered findings validation failed')
if index.count('| NAND program interference / 2002–2014 bounded planar-MLC regime |') != 1:
    raise SystemExit('Case 59 comparison row validation failed')

readme_p.write_text(readme, encoding='utf-8')
roadmap_p.write_text(roadmap, encoding='utf-8')
index_p.write_text(index, encoding='utf-8')

print('Case 59 integration patch validated: 60/60 grounded cases')
