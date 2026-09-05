from pathlib import Path
import re

CASE52 = Path('cases/52-nand-flash-read-disturb-access-induced-decay.md')
EVID52 = Path('evidence/52-cai-2009-2015-nand-read-disturb-grounding.md')
CASE97 = Path('cases/97-nand-flash-read-disturb-access-conditioned-retention.md')
EVID97 = Path('evidence/97-nand-2002-2015-read-disturb-grounding.md')
README = Path('README.md')
ROADMAP = Path('ROADMAP.md')
INDEX = Path('CASE_INDEX.md')


def replace_once(text, old, new, label):
    if old in text:
        return text.replace(old, new, 1)
    if new in text:
        return text
    raise SystemExit(f'{label}: expected anchor not found')


def sub_once(text, pattern, repl, label, flags=0):
    out, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n == 1:
        return out
    if repl in text:
        return text
    raise SystemExit(f'{label}: expected regex anchor not found')


# ---------------------------------------------------------------------------
# Canonical Case 52: absorb the unique historical evidence from duplicate 97.
# ---------------------------------------------------------------------------
s = CASE52.read_text()

status_new = """**`grounded`** — bounded to NAND read-disturb as documented from a Fujitsu 2002-priority manufacturer filing through Yu Cai et al.'s 2015 DSN experimental characterization. NASA/JPL's 2008 qualification study is retained as an independent institutional witness, including its explicit negative result, while a 2009-priority Texas Memory Systems patent and a 2013 APSys paper constrain controller/FTL prior-art claims. The case distinguishes measured device behavior from proposed controller mitigation/recovery and does not claim commercial deployment of the 2015 mechanisms.
"""
if 'Fujitsu 2002-priority manufacturer filing' not in s:
    s, n = re.subn(
        r"\*\*`grounded`\*\* — bounded to NAND read-disturb as documented before and through Yu Cai et al\.'s 2015 DSN experimental characterization.*?does not claim commercial deployment of the 2015 mechanisms\.\n",
        status_new,
        s,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise SystemExit('Case52 status paragraph anchor not found')

historical_insert = r'''### Fujitsu 2002-priority manufacturer witness

Fujitsu's **US20030137873A1, “Read disturb alleviated flash memory,”** has a 22 January 2002 priority date, was filed on 22 October 2002, and was published on 24 July 2003. The original assignee is Fujitsu Ltd. The application explicitly concerns NAND-type Flash and uses `read disturb` as period vocabulary. Its background explains that a high voltage is applied to non-selected word lines during read so that those cells conduct; this can place non-selected cells in a light-programming condition, add floating-gate charge, raise threshold voltage, and eventually compromise the erased/programmed distinction. The disclosed design varies the non-selected-word-line voltage and makes the tradeoff explicit: lowering that voltage can suppress disturb, but lowering it too far can make some cells fail to conduct correctly during read.

Source: <https://patents.google.com/patent/US20030137873A1/en>.

This is an earlier manufacturer-primary witness than the 2009-priority Texas Memory Systems patent used below. It is **not** evidence that Fujitsu first discovered read disturb or invented every later mitigation technique.

### NASA/JPL 2008 qualification witness and negative result

Douglas Sheldon and Michael Freie's NASA/JPL **_Disturb Testing in Flash Memories_**, JPL Publication 08-7 (March 2008), treats read disturb as a qualification/reliability problem for 2Gb NAND devices. It says manufacturers acknowledged disturb failures and supplied guidance, describes read disturb as a neighboring-cell/state problem within a block, and records a contemporary rule of thumb of roughly one million READ cycles per block for SLC and 100,000 for MLC. If an application had to exceed that guidance, the report recommended moving the data to another block and erasing the original block, thereby restarting that block's read-disturb exposure cycle.

Source: <https://nepp.nasa.gov/files/13582/07-100%20Sheldon_JPL%20Distrub%20Testing%20in%20Flash%20Mem.pdf>.

The same report is especially valuable because it preserves a **negative result**. Its read-disturb program performed 50k, 100k, 500k, and 1M page-read operations on a single page, yet the conclusions state that no program-disturb or read-disturb failures were detected in the tested devices. Therefore the report's read-count figures are historical guidance, not universal physical thresholds.

'''
anchor = '## Historical vocabulary and record\n\n'
if '### Fujitsu 2002-priority manufacturer witness' not in s:
    if anchor not in s:
        raise SystemExit('Case52 historical-record anchor not found')
    s = s.replace(anchor, anchor + historical_insert, 1)

s = s.replace('### Recognized `Read Disturb` before 2015', '### Additional controller prior art and open characterization, 2009–2015', 1)

negative_insert = r'''### A mechanism does not imply one universal read-count failure threshold

The 2008 NASA/JPL report supplies a useful counterexample to threshold universalization. It treated large read counts as a reliability stress and recommended migration/erase when contemporary guidance had to be exceeded, yet its own 2Gb-device test detected no read-disturb failure after the tested 50k, 100k, 500k, and 1M single-page read sequences.

Therefore:

> **read-disturb mechanism ≠ universal fixed read-count failure threshold**.

Any operational threshold must be qualified by device generation, process, wear, data pattern, temperature, voltage, ECC margin, and test/workload conditions. The report's numbers are retained as 2008 guidance, not as constants for later NAND.

'''
anchor = '### Read count can become a maintenance clock\n'
if '### A mechanism does not imply one universal read-count failure threshold' not in s:
    if anchor not in s:
        raise SystemExit('Case52 read-count anchor not found')
    s = s.replace(anchor, negative_insert + anchor, 1)

metadata_insert = r'''### A bounded maintenance summary can be tiny relative to payload

Cai et al.'s proposed `Vpass Tuning` implementation gives a bounded example of retained controller state: one byte per block for the tuned `Vpass` setting and one byte for the predicted worst-case page. In the paper's assumed 512GB / 65,536-block configuration, that is 128KB total metadata.

This is a research-design cost estimate, not a universal commercial SSD format. Its methodological use is narrower:

> **small maintenance metadata ≠ small retention significance**.

A controller need not archive every read event to make access-conditioned maintenance decisions; a compact counter, voltage setting, error-margin estimate, or worst-case-page summary can be operationally constitutive while remaining distinct from user payload.

'''
anchor = '### Recovery can use additional disturbance as diagnostic evidence\n'
if '### A bounded maintenance summary can be tiny relative to payload' not in s:
    if anchor not in s:
        raise SystemExit('Case52 RDR anchor not found')
    s = s.replace(anchor, metadata_insert + anchor, 1)

case67_insert = r'''### Versus Case 67 — later 3-D NAND adaptive read reclaim

Case 52 is the canonical physical/access-induced read-disturb case and now carries the 2002–2015 historical bridge. Case 67 remains a distinct later controller-policy slice: a 2017-priority / 2019 SK hynix disclosure uses compressed read-count proxies, thresholded ECC qualification, adaptive future checking, 3-D neighborhood sampling, and conditional reclaim. In that design a maintenance proxy can even be cleared at power-off while the physical disturb condition persists.

Therefore:

> **generic read-disturb mechanism/history ≠ one later 3-D NAND controller policy**.

The cases should be compared, not duplicated or silently merged into one universal controller design.

'''
anchor = '## Read semantics compared with magnetic core\n'
if '### Versus Case 67 — later 3-D NAND adaptive read reclaim' not in s:
    if anchor not in s:
        raise SystemExit('Case52 core-comparison anchor not found')
    s = s.replace(anchor, case67_insert + anchor, 1)

claim_anchor = '| NAND `Read Disturb` vocabulary and read-count-based mitigation predate 2015 | H/P | 2009-priority US7818525B1 + 2013 APSys record |'
claim_rows = r'''| NAND `read disturb` vocabulary and pass-voltage tradeoff are documented in a Fujitsu 2002-priority filing | H/P | US20030137873A1 / US6707714B2 |
| NASA/JPL treated disturb as a NAND reliability/qualification problem in 2008 and reported no disturb failures in its tested devices | H/S | JPL Publication 08-7, executive summary + Program 8 + conclusions |
| A fixed universal NAND read-count failure threshold follows from the existence of read disturb | X | JPL 2008 negative result plus process/wear/device dependence block that upgrade |
'''
if 'Fujitsu 2002-priority filing | H/P | US20030137873A1' not in s:
    if claim_anchor not in s:
        raise SystemExit('Case52 claim-ledger anchor not found')
    s = s.replace(claim_anchor, claim_rows + claim_anchor, 1)

CASE52.write_text(s)


# ---------------------------------------------------------------------------
# Evidence 52: preserve stable path while expanding the evidence window.
# ---------------------------------------------------------------------------
s = EVID52.read_text()
s = s.replace('# Case 52 Grounding Record — NAND Read Disturb, 2009–2015', '# Case 52 Grounding Record — NAND Read Disturb, 2002–2015', 1)

consolidation_note = r'''## Consolidation note

This grounding record keeps its existing filename for stable links, but its evidence window is now **2002–2015**. The former Case 97 duplicated Case 52's central mechanism and has therefore been removed from the live case ledger. Its genuinely additional evidence has been absorbed here: Fujitsu's 2002-priority manufacturer filing and NASA/JPL's 2008 qualification/test report, including the report's explicit no-disturb-failure result. Git history retains the former files for provenance.

This consolidation does not merge Case 67. Case 67 remains a later, bounded 3-D NAND controller-policy case rather than another generic read-disturb history.

'''
anchor = '## Evidence classes\n'
if '## Consolidation note' not in s:
    if anchor not in s:
        raise SystemExit('Evidence52 evidence-classes anchor not found')
    s = s.replace(anchor, consolidation_note + anchor, 1)

# Add earlier evidence rows immediately after the evidence-table separator.
rows = r'''| Fujitsu, US20030137873A1 / US6707714B2 | priority 2002-01-22; publication 2003-07-24 | manufacturer primary patent | early explicit NAND `read disturb` vocabulary; non-selected-word-line read voltage; light-programming / threshold-shift mechanism; voltage tradeoff | first discovery/invention priority; universal later-controller implementation |
| Sheldon & Freie, NASA/JPL Publication 08-7 | March 2008 | institutional qualification/test report | disturb as a reliability concern; migration+erase guidance; 50k/100k/500k/1M read protocol; explicit no-disturb-failure result | universal read-count threshold; evidence that the tested devices actually failed from read disturb |
'''
if '| Fujitsu, US20030137873A1 / US6707714B2 |' not in s:
    table_header = '| --- | --- | --- | --- | --- |\n'
    if table_header not in s:
        raise SystemExit('Evidence52 table separator not found')
    s = s.replace(table_header, table_header + rows, 1)

prior_sections = r'''## Earlier manufacturer-primary evidence — Fujitsu 2002/2003

Fujitsu Limited, **“Read disturb alleviated flash memory,”** US20030137873A1 / US6707714B2:

- priority: 22 January 2002;
- U.S. filing: 22 October 2002;
- U.S. application publication: 24 July 2003;
- original assignee: Fujitsu Ltd.

Source: <https://patents.google.com/patent/US20030137873A1/en>.

Directly inspected patent metadata and description support the following bounded historical claims: the application explicitly concerns NAND-type Flash and uses `read disturb`; NAND read applies a high voltage to non-selected word lines so non-selected cells conduct; the background describes a light-programming condition in which floating-gate charge and threshold voltage can rise; and the disclosed voltage-control scheme treats lower non-selected-word-line voltage as a disturb/read-margin tradeoff.

Evidence strength: **H/P — strong for date, vocabulary, mechanism class, and tradeoff.** It does not establish first discovery or first invention of read disturb.

## Independent institutional qualification evidence — NASA/JPL 2008

Douglas Sheldon and Michael Freie, **_Disturb Testing in Flash Memories_**, JPL Publication 08-7, March 2008, NASA Electronic Parts and Packaging (NEPP) Program.

Source: <https://nepp.nasa.gov/files/13582/07-100%20Sheldon_JPL%20Distrub%20Testing%20in%20Flash%20Mem.pdf>.

Directly relevant anchors:

- the executive summary defines disturb testing as asking whether programming or reading nearby cells changes an initially expected stored state, states that manufacturers acknowledged disturb failures, and says **no specific disturb failures were noted in the report's testing**;
- the disturb-errors discussion gives a contemporary rule of thumb of no more than roughly one million READ cycles per block for SLC and 100,000 for MLC, and recommends moving data to another block and erasing the original if the application must exceed that guidance;
- Program 8 performs 50k, 100k, 500k, and 1M page reads on a single page;
- the conclusions state that no program-disturb or read-disturb failures were detected in the tested devices.

Evidence strength: **H/S — strong institutional test/qualification witness and especially strong as a negative-result boundary.** The numerical guidance is retained as period guidance, not a universal NAND law.

Retention-specific result:

> **recognized failure mechanism + conservative engineering guidance ≠ a fixed failure threshold reproduced by every tested device**.

'''
anchor = '## Primary paper inspected\n'
if '## Earlier manufacturer-primary evidence — Fujitsu 2002/2003' not in s:
    if anchor not in s:
        raise SystemExit('Evidence52 primary-paper anchor not found')
    s = s.replace(anchor, prior_sections + anchor, 1)

if 'After consolidation, the evidence chain begins with Fujitsu' not in s:
    anchor = '## Grounding decision\n\n'
    note = ('After consolidation, the evidence chain begins with Fujitsu\'s 2002-priority manufacturer filing and NASA/JPL\'s independent 2008 qualification/test record, then continues through the 2009-priority controller patent, 2013 peer-reviewed prior-art record, and 2015 commercial-chip characterization. The expanded chronology strengthens the case without changing the boundary between historical evidence and proposed 2015 mechanisms.\n\n')
    if anchor not in s:
        raise SystemExit('Evidence52 grounding-decision anchor not found')
    s = s.replace(anchor, anchor + note, 1)

EVID52.write_text(s)


# ---------------------------------------------------------------------------
# README: one canonical navigation entry, no duplicate Case 97 entry.
# ---------------------------------------------------------------------------
s = README.read_text()
case52_readme = "- [`cases/52-nand-flash-read-disturb-access-induced-decay.md`](cases/52-nand-flash-read-disturb-access-induced-decay.md) — grounded canonical NAND read-disturb case, now deepened across 2002–2015: Fujitsu's 2002-priority manufacturer filing anchors early period vocabulary and read-voltage tradeoffs; NASA/JPL 2008 supplies independent qualification guidance plus an explicit no-disturb-failure test result; 2009/2013 prior art and Cai et al. 2015 preserve the controller/experimental boundaries. The case separates access-conditioned disturbance from retention-age loss, ECC-correct output from unchanged physical state, and compact maintenance summaries from complete read history; see [`evidence/52-cai-2009-2015-nand-read-disturb-grounding.md`](evidence/52-cai-2009-2015-nand-read-disturb-grounding.md)."
pattern = r'^- \[`cases/52-nand-flash-read-disturb-access-induced-decay\.md`\].*$'
s, n = re.subn(pattern, case52_readme, s, count=1, flags=re.M)
if n != 1 and case52_readme not in s:
    raise SystemExit('README Case52 entry not found')

s = '\n'.join(
    line for line in s.splitlines()
    if 'cases/97-nand-flash-read-disturb-access-conditioned-retention.md' not in line
    and 'evidence/97-nand-2002-2015-read-disturb-grounding.md' not in line
) + '\n'
README.write_text(s)


# ---------------------------------------------------------------------------
# ROADMAP: turn the duplicate line into an explicit consolidation/deepening.
# ---------------------------------------------------------------------------
s = ROADMAP.read_text()
roadmap_note = "- [x] NAND Flash read-disturb historical deepening / duplicate consolidation — canonical [`cases/52-nand-flash-read-disturb-access-induced-decay.md`](cases/52-nand-flash-read-disturb-access-induced-decay.md), with its stable [`evidence/52-cai-2009-2015-nand-read-disturb-grounding.md`](evidence/52-cai-2009-2015-nand-read-disturb-grounding.md) path, now absorbs the unique 2002–2008 evidence previously duplicated in Case 97: Fujitsu 2002-priority manufacturer vocabulary/mechanism evidence and NASA/JPL 2008 qualification testing, including an explicit no-disturb-failure result after the tested read sequences. Case 67 remains the distinct later 3-D NAND adaptive-reclaim policy slice. Broader NAND/3D-NAND/controller genealogy, named commercial deployment, and device-specific threshold validation remain open and should be coordinated with `computing-archaeology`."
pattern = r'^- \[x\] NAND Flash read-disturb / access-conditioned retention bridge — .*cases/97-nand-flash-read-disturb-access-conditioned-retention\.md.*$'
s, n = re.subn(pattern, roadmap_note, s, count=1, flags=re.M)
if n != 1 and roadmap_note not in s:
    raise SystemExit('ROADMAP Case97 line not found')
ROADMAP.write_text(s)


# ---------------------------------------------------------------------------
# CASE_INDEX: update canonical row, remove duplicate ledger row, retain useful
# comparison/findings as Case 52 deepening, and correct aggregate count.
# ---------------------------------------------------------------------------
s = INDEX.read_text()
case52_index = "| [NAND Flash Read Disturb: Access-Induced Decay, Vpass Mitigation, and Recovery](cases/52-nand-flash-read-disturb-access-induced-decay.md) | **grounded** | selected-page read + elevated `Vpass` on unselected same-block cells + cumulative read-count stress + threshold-voltage drift + ECC margin + optional compact maintenance metadata / relocation / RDR | separate present read success from future neighbor-retention cost; access-conditioned disturbance from retention-age refresh; selected-page nondestructiveness from zero material disturbance elsewhere; historical mechanism/guidance from universal thresholds; measured chip behavior from proposed controller mitigation/recovery | [expanded 2002–2015 NAND read-disturb grounding](evidence/52-cai-2009-2015-nand-read-disturb-grounding.md); Case 67 covers later 3-D NAND adaptive read reclaim, while broader controller genealogy, named-product deployment, and independent fault validation remain separate work |"
pattern = r'^\| \[NAND Flash Read Disturb: Access-Induced Decay, Vpass Mitigation, and Recovery\]\(cases/52-nand-flash-read-disturb-access-induced-decay\.md\).*$'
s, n = re.subn(pattern, case52_index, s, count=1, flags=re.M)
if n != 1 and case52_index not in s:
    raise SystemExit('CASE_INDEX Case52 ledger row not found')

# Remove the duplicate Case97 ledger row.
s, n = re.subn(r'^\| \[NAND Flash Read Disturb: Access-Conditioned Retention and Neighbor-State Maintenance\]\(cases/97-nand-flash-read-disturb-access-conditioned-retention\.md\).*$\n?', '', s, count=1, flags=re.M)
if n != 1 and 'cases/97-nand-flash-read-disturb-access-conditioned-retention.md' in s:
    raise SystemExit('CASE_INDEX Case97 ledger row not removed')

# Preserve the useful matrix regime, but make its canonical ownership explicit.
s = s.replace('| NAND read disturb / 2002–2015 bounded regime |', '| NAND read disturb / 2002–2015 bounded regime (Case 52 canonical) |', 1)

s = s.replace('### Case 97 — NAND Flash read-disturb findings', '### Case 52 historical deepening — 2002–2015 NAND Flash read-disturb findings', 1)
s = s.replace('**maintenance can be caused by use rather than waiting** — Case 97 adds an access-triggered nonvolatile-memory regime', '**maintenance can be caused by use rather than waiting** — Case 52\'s 2002–2015 deepening adds an access-triggered nonvolatile-memory regime', 1)

for old, new in [
    ('96 bounded cases, 96 of them `grounded`', '95 bounded cases, 95 of them `grounded`'),
    ('96 bounded cases, all 96 `grounded`', '95 bounded cases, all 95 `grounded`'),
    ('96 canonical cases', '95 canonical cases'),
    ('96 bounded cases, 96 grounded', '95 bounded cases, 95 grounded'),
]:
    s = s.replace(old, new)

INDEX.write_text(s)

# Correct aggregate wording elsewhere if present.
for p in [README, ROADMAP]:
    t = p.read_text()
    for old, new in [
        ('96 bounded cases, 96 of them `grounded`', '95 bounded cases, 95 of them `grounded`'),
        ('96 bounded cases, all 96 `grounded`', '95 bounded cases, all 95 `grounded`'),
        ('96 canonical cases', '95 canonical cases'),
        ('96 bounded cases, 96 grounded', '95 bounded cases, 95 grounded'),
    ]:
        t = t.replace(old, new)
    p.write_text(t)


# ---------------------------------------------------------------------------
# Remove duplicate current-tree files only after their unique evidence is merged.
# Git history retains the original Case 97 provenance.
# ---------------------------------------------------------------------------
if CASE97.exists():
    CASE97.unlink()
if EVID97.exists():
    EVID97.unlink()


# ---------------------------------------------------------------------------
# Sanity checks: canonical files remain, duplicate paths vanish, evidence is
# present, navigation is coherent, and count returns to 95 canonical cases.
# ---------------------------------------------------------------------------
assert CASE52.exists()
assert EVID52.exists()
assert not CASE97.exists()
assert not EVID97.exists()

case52_text = CASE52.read_text()
evid52_text = EVID52.read_text()
assert '### Fujitsu 2002-priority manufacturer witness' in case52_text
assert '### NASA/JPL 2008 qualification witness and negative result' in case52_text
assert 'read-disturb mechanism ≠ universal fixed read-count failure threshold' in case52_text
assert '### Versus Case 67 — later 3-D NAND adaptive read reclaim' in case52_text
assert '# Case 52 Grounding Record — NAND Read Disturb, 2002–2015' in evid52_text
assert '## Earlier manufacturer-primary evidence — Fujitsu 2002/2003' in evid52_text
assert '## Independent institutional qualification evidence — NASA/JPL 2008' in evid52_text

for p in [README, ROADMAP, INDEX]:
    t = p.read_text()
    if 'cases/97-nand-flash-read-disturb-access-conditioned-retention.md' in t or 'evidence/97-nand-2002-2015-read-disturb-grounding.md' in t:
        raise SystemExit(f'{p}: stale Case97 path remains')

idx = INDEX.read_text()
assert '### Case 52 historical deepening — 2002–2015 NAND Flash read-disturb findings' in idx
assert '| NAND read disturb / 2002–2015 bounded regime (Case 52 canonical) |' in idx
assert '95 bounded cases' in idx or '95 canonical cases' in idx

# No live Markdown document should still navigate to the removed duplicate paths.
for p in Path('.').rglob('*.md'):
    t = p.read_text(errors='replace')
    if 'cases/97-nand-flash-read-disturb-access-conditioned-retention.md' in t or 'evidence/97-nand-2002-2015-read-disturb-grounding.md' in t:
        raise SystemExit(f'stale duplicate reference remains in {p}')
