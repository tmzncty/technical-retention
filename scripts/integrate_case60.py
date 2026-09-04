from pathlib import Path
import re

ROOT = Path('.')
readme_p = ROOT / 'README.md'
roadmap_p = ROOT / 'ROADMAP.md'
index_p = ROOT / 'CASE_INDEX.md'

readme = readme_p.read_text(encoding='utf-8')
roadmap = roadmap_p.read_text(encoding='utf-8')
index = index_p.read_text(encoding='utf-8')

case_path = 'cases/60-apollo-core-rope-wired-topology.md'
evidence_path = 'evidence/60-apollo-core-rope-1964-1972-grounding.md'

# README navigation: append Case 60 immediately after Case 59.
readme_line = (
    '- [`cases/60-apollo-core-rope-wired-topology.md`]'
    '(cases/60-apollo-core-rope-wired-topology.md) — grounded Apollo core-rope bridge: '
    'the AGC fixed program is encoded by sense-wire thread/bypass geometry while selected ferrite cores switch and reset during read; '
    'this separates state-bearing topology from magnetic access transduction and from classic destructive-read core RAM, while 1964–1966 wired-core prior art bounds novelty.\n'
)
if case_path not in readme:
    lines = readme.splitlines(keepends=True)
    out = []
    inserted = False
    for line in lines:
        out.append(line)
        if 'cases/59-nand-program-interference-write-induced-neighbor-drift.md' in line:
            out.append(readme_line)
            inserted = True
    if not inserted:
        raise SystemExit('README Case 59 anchor not found')
    readme = ''.join(out)

# ROADMAP: add a bounded magnetic-core -> wired-core fixed-topology bridge before ROM -> PROM.
roadmap_bullet = (
    '- [x] magnetic-core retained state → wired-core fixed topology — the bounded contrast is now grounded by '
    '[`cases/02-magnetic-core-destructive-read.md`](cases/02-magnetic-core-destructive-read.md) and '
    '[`cases/60-apollo-core-rope-wired-topology.md`](cases/60-apollo-core-rope-wired-topology.md), with Case 60 grounded by '
    '[`evidence/60-apollo-core-rope-1964-1972-grounding.md`](evidence/60-apollo-core-rope-1964-1972-grounding.md). '
    'Case 02 uses classic coincident-current RAM to show remanent magnetization as payload plus destructive-read/rewrite semantics. '
    'Case 60 uses the Block II Apollo Guidance Computer to show a different ferrite regime: the fixed program bit is the manufactured '
    'sense-wire thread/bypass relation, while the selected core switches and resets as a transformer/read transducer. MIT R-700 and '
    'NASA SP-8070 also move ordinary program revision out of runtime electrical write service and into physical module manufacture, '
    'verification, and replacement; contemporary 1964–1966 wired-core records prevent an Apollo invention claim. This checkbox closes '
    'only the retention-specific contrast `magnetic material ≠ magnetic-state payload`; the broader wired-memory/transformer-ROM genealogy, '
    'mission-specific production archaeology, and semiconductor-ROM descent remain separate future work;\n'
)
if case_path not in roadmap:
    anchor = '- [x] ROM → PROM → EPROM → EEPROM → Flash'
    pos = roadmap.find(anchor)
    if pos < 0:
        raise SystemExit('ROADMAP ROM bridge anchor not found')
    roadmap = roadmap[:pos] + roadmap_bullet + roadmap[pos:]

# CASE_INDEX case ledger row, immediately after Case 59.
case_row = (
    '| [Apollo Guidance Computer Core Rope: Fixed Program State in Wiring Topology]'
    '(cases/60-apollo-core-rope-wired-topology.md) | **grounded** | '
    'manufactured sense-wire/core thread-bypass topology + ferrite transformer switching/reset + inhibit/address wiring + modular replacement | '
    'separate state-bearing relation from state-changing read transducer; logical nondestructive read from zero physical change; runtime read-only semantics from physical immutability; and quiescent retention work from production/verification labor | '
    '[1964–1972 Apollo core-rope grounding](evidence/60-apollo-core-rope-1964-1972-grounding.md); pre-Apollo wired-memory genealogy, mission-specific rope production/configuration records, exact flight-module fault archaeology, and physical reconstruction remain separate work |\n'
)
if case_path not in index:
    lines = index.splitlines(keepends=True)
    out = []
    inserted = False
    for line in lines:
        out.append(line)
        if line.startswith('| [') and 'cases/59-nand-program-interference-write-induced-neighbor-drift.md' in line:
            out.append(case_row)
            inserted = True
    if not inserted:
        raise SystemExit('CASE_INDEX Case 59 row anchor not found')
    index = ''.join(out)

# Comparison matrix row: place after the classic Magnetic core row to expose the mechanism contrast.
matrix_row = (
    '| Apollo AGC core rope / wired-in fixed memory | '
    'sense-wire thread/bypass geometry around ferrite cores + inhibit/address-selection wiring; core magnetic state is read transduction rather than the fixed payload bit | '
    'no periodic rewriting merely to preserve the fixed program; manufacturing/verification before service and module replacement for revision; selected core still undergoes set/reset switching during each read | '
    'logically nondestructive fixed-memory read even though the selected core changes magnetic state and is reset | '
    'fixed-memory address decoded through set/reset + inhibit selection, then selected sense-line group; addressability infrastructure is distinct from payload topology | '
    'high within one manufactured module; current program can change by replacing the module while an old module remains readable | '
    'no operational history by default; a superseded physical rope may preserve an obsolete complete program image |\n'
)
if '| Apollo AGC core rope / wired-in fixed memory |' not in index:
    mstart = index.find('## Comparison matrix')
    if mstart < 0:
        raise SystemExit('comparison matrix heading not found')
    mend = index.find('\n## ', mstart + len('## Comparison matrix'))
    if mend < 0:
        mend = len(index)
    segment = index[mstart:mend]
    seg_lines = segment.splitlines(keepends=True)
    pos = None
    for i, line in enumerate(seg_lines):
        if line.startswith('| Magnetic core |'):
            pos = i + 1
            break
    if pos is None:
        raise SystemExit('classic Magnetic core comparison row not found')
    seg_lines.insert(pos, matrix_row)
    index = index[:mstart] + ''.join(seg_lines) + index[mend:]

# Case 60 cross-case findings. Continue the monotonic finding ledger after Case 59 finding 635.
findings = '''\n\n## Case 60 — Apollo core-rope findings\n\n636. **State-bearing structure ≠ state-changing transducer.** In the bounded AGC fixed-memory regime, the program bit is encoded by a sense conductor's thread/bypass relation while the selected ferrite core intentionally switches during readout.\n637. **Ferrite-core switching during read ≠ destructive logical read.** The selected core is set and reset, but the fixed program remains because the bit-defining topology is not rewritten by that magnetic cycle.\n638. **Use of magnetic material ≠ magnetic-state payload retention.** Case 02 and Case 60 both use ferrite switching physics, yet one retains the bit in remanent polarity and the other uses the core principally as a transformer/read transducer for wired geometry.\n639. **Read-only at runtime ≠ physically immutable artifact.** Ordinary AGC program steps cannot rewrite rope contents, while humans can manufacture, rework, replace, damage, or destroy the module.\n640. **Program supersession ≠ physical disappearance of the superseded program artifact.** A replaced rope can remain fully readable even though another installed module has become the current flight program.\n641. **Manufacturing correctness can be information correctness.** In a geometry-coded memory, a routing error can directly become a wrong stored bit rather than merely a packaging defect around an otherwise correct state.\n642. **Write semantics can migrate from runtime command to fabrication workflow.** Changing the fixed program means producing a new physical wiring configuration rather than issuing an ordinary electrical write instruction.\n643. **Low quiescent retention work ≠ low lifecycle retention labor.** Core rope needs no periodic payload refresh merely to keep the fixed program, while substantial labor moves into bit-pattern preparation, routing, assembly, verification, configuration control, and replacement.\n644. **Revision latency ≠ read latency ≠ retention interval.** NASA's bounded Apollo witness of an approximately four-week program-change production cycle describes update/replacement time, not the time to read a word or a universal shelf-retention duration.\n645. **Payload topology ≠ recoverability infrastructure.** Sense-line routing carries fixed bits, while set/reset, inhibit, diode/switching, and sense-selection paths determine whether the encoded relation can be addressed and recovered.\n646. **One ferrite core ≠ one stored bit.** The bounded Block II rope organization lets many sense lines thread or bypass one selected core, so a core participates in many fixed bits rather than carrying a single bit through its own remanence.\n647. **Shared material family ≠ shared retention semantics.** Calling both Case 02 and Case 60 `core memory` is insufficient to characterize what remains, what read changes, and what operation constitutes rewrite.\n648. **Manufactured fixed pattern ≈ mask ROM only as a functional analogy.** Both can expose ordinary-runtime read-only state, but core-rope magnetic transformer coupling and semiconductor mask-ROM fabrication are different mechanisms; no direct genealogy is established here.\n649. **Apollo core rope ≠ invention of wired-in fixed memory.** Nelson's 1964-filed wired-core patent and MIT's own 1966-filed wired-in-memory manufacturing patent place geometry-coded fixed memories in a broader contemporary prior-art field.\n650. **Reduced accidental runtime rewrite risk ≠ maintenance-free or revision-free retention.** Fixedness suppresses one class of in-service modification by moving change authority and correctness work into manufacturing, verification, module logistics, and physical replacement.\n'''
if '## Case 60 — Apollo core-rope findings' not in index:
    anchor = '635. **2013 commercial-chip characterization ≠ invention of NAND cell-to-cell interference or program-order mitigation.**'
    p = index.find(anchor)
    if p < 0:
        raise SystemExit('Case 59 finding 635 anchor not found')
    line_end = index.find('\n', p)
    if line_end < 0:
        line_end = len(index)
    index = index[:line_end] + findings + index[line_end:]

# Conservative count wording updates where summaries already state total case counts.
for old, new in [
    ('60 bounded cases', '61 bounded cases'),
    ('60 grounded cases', '61 grounded cases'),
    ('sixty bounded cases', 'sixty-one bounded cases'),
    ('sixty grounded cases', 'sixty-one grounded cases'),
]:
    index = index.replace(old, new)
    readme = readme.replace(old, new)
    roadmap = roadmap.replace(old, new)

# Validate navigation and ledger before writing.
case_table = index.split('## Cases', 1)[1].split('\n---\n', 1)[0]
paths = re.findall(r'\(cases/(\d{2})-[^)]+\.md\)', case_table)
expected = {f'{i:02d}' for i in range(61)}
if len(paths) != 61 or len(set(paths)) != 61 or set(paths) != expected:
    raise SystemExit(f'case ledger validation failed: count={len(paths)} unique={len(set(paths))} tail={paths[-5:]}')
if case_table.count('**grounded**') != 61:
    raise SystemExit(f'grounded case count validation failed: {case_table.count("**grounded**")}')
if readme.count(case_path) != 2:
    raise SystemExit(f'README case-path count unexpected: {readme.count(case_path)}')
if roadmap.count(case_path) != 2:
    raise SystemExit(f'ROADMAP case-path count unexpected: {roadmap.count(case_path)}')
if case_table.count(case_path) != 1:
    raise SystemExit(f'CASE_INDEX case-table path count unexpected: {case_table.count(case_path)}')
if case_table.count(evidence_path) != 1:
    raise SystemExit(f'CASE_INDEX evidence path count unexpected: {case_table.count(evidence_path)}')
if index.count('## Case 60 — Apollo core-rope findings') != 1:
    raise SystemExit('Case 60 findings missing/duplicated')
if index.count('636. **State-bearing structure') != 1 or index.count('650. **Reduced accidental runtime rewrite risk') != 1:
    raise SystemExit('Case 60 numbered findings validation failed')
if index.count('| Apollo AGC core rope / wired-in fixed memory |') != 1:
    raise SystemExit('Case 60 comparison row validation failed')

readme_p.write_text(readme, encoding='utf-8')
roadmap_p.write_text(roadmap, encoding='utf-8')
index_p.write_text(index, encoding='utf-8')

print('Case 60 integration patch validated: 61/61 grounded cases')
