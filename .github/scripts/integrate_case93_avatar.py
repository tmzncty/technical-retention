from pathlib import Path
import re

CASE = Path('cases/93-dram-variable-retention-time-profile-staleness.md')
ROADMAP = Path('ROADMAP.md')
INDEX = Path('CASE_INDEX.md')
ADDENDUM = 'evidence/93-avatar-2015-vrt-aware-refresh-revalidation-deepening.md'

# --- Case 93 ---
case = CASE.read_text(encoding='utf-8')
lines = case.splitlines()
for i, line in enumerate(lines):
    if line.startswith('- **Bounded system:**') and 'RAIDR' in line:
        lines[i] = ('- **Bounded system:** DRAM retention-time profiling as represented by the 2012 RAIDR proposal, '
                    'stressed against variable-retention-time (VRT) and data-pattern-dependence (DPD) evidence from period '
                    'device research and the 2013 commodity-DDR3 characterization, then bounded by the 2015 AVATAR research '
                    'proposal as a concrete runtime requalification response.')
        break
case = '\n'.join(lines) + '\n'

avatar_section = '''### H/P — 2015 AVATAR turns runtime error evidence into refresh-class revision

Qureshi et al.'s 2015 DSN paper **AVATAR** is a useful later boundary because it does not assume that a stored retention profile stays authoritative forever. Its multirate-refresh design retains a per-row **Refresh Rate Table (RRT)**, uses ECC plus proactive memory scrubbing to expose runtime failures, upgrades the containing row to Fast Refresh after an ECC correction, and uses separate infrequent retention testing to permit later downgrade to Slow Refresh.

The paper also discusses storing the RRT itself in a reserved DRAM region and triplicating that control state in the evaluated design option. This makes the second-order retention relation explicit: metadata that decides how aggressively DRAM is preserved may itself reside in, and require protection from errors in, the memory it controls.

The important boundary is not the paper's particular evaluated intervals. It is the state/evidence path:

```text
initial retention test
    -> retained row refresh class
    -> runtime VRT transition may make that class unsafe
    -> ECC/access or proactive scrub exposes an error
    -> conservative upgrade to faster refresh
    -> separate later retention test may authorize downgrade
```

Thus **error correction ≠ unique fault-cause diagnosis**, **ECC capability ≠ observation coverage**, **scrub ≠ refresh**, and **maintenance-class persistence ≠ maintenance-class immutability**. The paper explicitly notes that ECC corrections can also arise from soft errors; the upgrade rule is conservative rather than a perfect VRT classifier.

This is a peer-reviewed architecture proposal/evaluation, not evidence of commodity deployment or a JEDEC requirement. Exact source anchors and the deployment boundary are recorded in [`../evidence/93-avatar-2015-vrt-aware-refresh-revalidation-deepening.md`](../evidence/93-avatar-2015-vrt-aware-refresh-revalidation-deepening.md).

'''
marker = '---\n\n## Retained state'
if ADDENDUM not in case:
    if marker not in case:
        raise AssertionError('Case 93 retained-state marker not found')
    case = case.replace(marker, avatar_section + '---\n\n## Retained state', 1)
CASE.write_text(case.rstrip() + '\n', encoding='utf-8')

# --- ROADMAP ---
roadmap = ROADMAP.read_text(encoding='utf-8')
r_lines = roadmap.splitlines()
phase2_entry = ('- [x] Case 93 AVATAR VRT-aware runtime-requalification deepening — canonical '
                '[`cases/93-dram-variable-retention-time-profile-staleness.md`](cases/93-dram-variable-retention-time-profile-staleness.md), '
                'with new [`evidence/93-avatar-2015-vrt-aware-refresh-revalidation-deepening.md`](evidence/93-avatar-2015-vrt-aware-refresh-revalidation-deepening.md), '
                'adds the 2015 DSN AVATAR research design as a bounded response to the already-grounded profile-staleness problem: '
                'a per-row Refresh Rate Table is revised when ECC/access or proactive scrub exposes an error, conservative upgrade to '
                'Fast Refresh is separated from later retest-authorized downgrade, and the paper even discusses DRAM-resident triplicated '
                'RRT state. This closes only the research-proposal relation `profile persistence != profile authority != observation coverage '
                '!= policy reclassification`; production deployment, JEDEC adoption, modern on-die-ECC visibility, DDR4/DDR5 controller '
                'implementations, and broader adaptive-refresh genealogy remain open and should be coordinated with `computing-archaeology`.')
if 'Case 93 AVATAR VRT-aware runtime-requalification deepening' not in roadmap:
    insert_at = None
    for i, line in enumerate(r_lines):
        if line.startswith('- [x] Case 59 pre-2002 NAND'):
            insert_at = i
            break
    if insert_at is None:
        raise AssertionError('Phase-2 Case 59 anchor not found')
    r_lines.insert(insert_at, phase2_entry)

new_refresh_failure = ('- [ ] refresh failure — **further advanced by grounded Cases 53 and 93, including a bounded 2015 '
                       'runtime-requalification research response**: Case 53 shows that the ordinary recurring refresh schedule can remain '
                       'present while repeated neighboring-row activation accelerates victim leakage enough to outrun that schedule; Case 93 '
                       'shows that a controller can faithfully execute a retention-aware schedule while the retained profile authorizing that '
                       'schedule has become non-conservative because of VRT, DPD, or an incomplete profiling window. The AVATAR deepening '
                       'adds one concrete proposal in which ECC/access and proactive scrub generate runtime evidence, affected rows are '
                       'conservatively upgraded to faster refresh, and a separate later retention test can authorize downgrade. This grounds '
                       '`profile persistence != profile authority`, `ECC capability != observation coverage`, `scrub != refresh`, and '
                       '`conservative upgrade authority != downgrade authority` without treating an ECC correction as perfect VRT diagnosis. '
                       'Missed ordinary refresh, self-refresh collapse, controller scheduling faults, modern TRR/RFM failures, production '
                       'adaptive-profiling evidence, JEDEC/vendor implementation history, and standards-specific refresh-management genealogy remain open;')
replaced = False
for i, line in enumerate(r_lines):
    if line.startswith('- [ ] refresh failure —'):
        r_lines[i] = new_refresh_failure
        replaced = True
        break
if not replaced and 'runtime-requalification research response' not in '\n'.join(r_lines):
    raise AssertionError('ROADMAP refresh-failure line not found')
ROADMAP.write_text('\n'.join(r_lines).rstrip() + '\n', encoding='utf-8')

# --- CASE_INDEX ---
index = INDEX.read_text(encoding='utf-8')
i_lines = index.splitlines()
new_row = ('| [DRAM Variable Retention Time: Profile Staleness and Unstable Preservation Deadlines]'
           '(cases/93-dram-variable-retention-time-profile-staleness.md) | **grounded** | volatile DRAM charge + retention-time profiling '
           '+ retained row/refresh classification + VRT/DPD-dependent profile uncertainty + runtime evidence-driven reclassification | '
           'separate physical retention behavior from the retained profile that governs maintenance; show preserved metadata can become stale; '
           'separate profile storage, profile authority, observation coverage, ECC correction, scrub evidence, and refresh-class revision | '
           '[1987–2013 VRT/profiling grounding](evidence/93-dram-1987-2013-vrt-profiling-grounding.md) + '
           '[2015 AVATAR runtime-requalification deepening](evidence/93-avatar-2015-vrt-aware-refresh-revalidation-deepening.md); exact '
           'transistor-defect genealogy, JEDEC/vendor screening, production adaptive profiling, later on-die ECC, DDR4/DDR5 standards/controllers, '
           'and deployment evidence remain separate work |')
row_done = False
for i, line in enumerate(i_lines):
    if '(cases/93-dram-variable-retention-time-profile-staleness.md)' in line and line.startswith('|'):
        i_lines[i] = new_row
        row_done = True
        break
if not row_done:
    raise AssertionError('Case 93 index row not found')
index = '\n'.join(i_lines).rstrip() + '\n'

heading = '## Case 93 deepening — AVATAR runtime requalification findings'
if heading not in index:
    if '**2414 —' not in index:
        raise AssertionError('expected previous finding 2414 missing')
    findings = '''
## Case 93 deepening — AVATAR runtime requalification findings

- **2415 — a retained refresh profile can become a mutable runtime control relation rather than a load-once artifact.** AVATAR retains per-row Fast/Slow refresh classification in an RRT and changes it when later evidence warrants a different maintenance rate. (`H/P`, `E`)
- **2416 — row identity continuity ≠ refresh-class continuity.** A row can keep the same address and payload role while its authorized maintenance interval changes after runtime evidence. (`E`)
- **2417 — retention-control metadata can itself require retention protection.** AVATAR discusses placing the RRT in reserved DRAM and triplicating it to tolerate errors in that control state; the policy representation is not outside the medium's reliability problem. (`H/P`, `E`)
- **2418 — RRT survival ≠ RRT authority.** Replicating or otherwise preserving the RRT protects its bits, but VRT can still make an intact row classification unsafe. (`E`, `X`)
- **2419 — ECC correction ≠ unique VRT diagnosis.** AVATAR upgrades a row after every ECC correction while explicitly acknowledging that some corrections can result from soft errors; the rule is conservative policy, not perfect causal identification. (`H/P`, `X`)
- **2420 — immediate correction and future maintenance reclassification are distinct effects of one error event.** ECC can repair the observed word while the same event separately causes the containing row to use Fast Refresh thereafter. (`H/P`, `E`)
- **2421 — ECC capability ≠ observation coverage.** If checking occurs only on ordinary access, low-activity regions can leave newly unsafe VRT state undiscovered; AVATAR therefore adds proactive memory scrub. (`H/P`, `E`)
- **2422 — scrub ≠ refresh.** In the bounded AVATAR design, refresh restores charge according to the current policy while scrub generates error evidence that may change that policy; both are maintenance but they have different semantics. (`H/P`, `E`, `X`)
- **2423 — physical VRT transition ≠ immediately revised control metadata.** A cell can enter a lower-retention state before ECC/access or scrub observes a resulting error, creating a separate observation-delay timescale. (`E`)
- **2424 — conservative upgrade authority ≠ downgrade authority.** AVATAR upgrades on an observed correction but proposes separate infrequent retention testing before allowing rows to return to Slow Refresh. (`H/P`, `E`)
- **2425 — evaluated scrub/retest intervals ≠ universal DRAM requirements.** The paper's 15-minute scrub and approximately yearly retest are design/evaluation choices, not JEDEC mandates or production-safe constants. (`H/P`, `X`)
- **2426 — AVATAR research design ≠ commodity deployment or complete adaptive-refresh genealogy.** The DSN 2015 paper directly grounds one architecture-level response to VRT profile staleness; current `computing-archaeology` searches expose no dedicated VRT/RAIDR/AVATAR case to reuse, and broader standards/product/manufacturing history remains routed there. (`H/P`, `X`)
'''
    index = index.rstrip() + '\n\n' + findings.lstrip('\n')
INDEX.write_text(index.rstrip() + '\n', encoding='utf-8')

# --- Validation ---
assert ADDENDUM in CASE.read_text(encoding='utf-8')
assert '2015 AVATAR research proposal' in CASE.read_text(encoding='utf-8')
assert 'Case 93 AVATAR VRT-aware runtime-requalification deepening' in ROADMAP.read_text(encoding='utf-8')
assert 'runtime-requalification research response' in ROADMAP.read_text(encoding='utf-8')
idx = INDEX.read_text(encoding='utf-8')
assert ADDENDUM in idx
for n in range(2415, 2427):
    count = len(re.findall(rf'\*\*{n} —', idx))
    assert count == 1, f'finding {n} count={count}'
