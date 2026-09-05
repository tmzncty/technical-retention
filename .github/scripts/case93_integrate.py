from pathlib import Path

CASE_PATH = 'cases/93-dram-variable-retention-time-profile-staleness.md'
EVID_PATH = 'evidence/93-dram-1987-2013-vrt-profiling-grounding.md'


def insert_after_line(text, needle, newline):
    if newline in text:
        return text
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if needle in line:
            lines.insert(i + 1, newline)
            return '\n'.join(lines) + ('\n' if text.endswith('\n') else '')
    raise RuntimeError(f'anchor not found: {needle}')


# README navigation
p = Path('README.md')
text = p.read_text()
readme_line = "- [`cases/93-dram-variable-retention-time-profile-staleness.md`](cases/93-dram-variable-retention-time-profile-staleness.md) — grounded DRAM profiling bridge: 2012 RAIDR makes refresh work depend on stored retention-time bins, while 2013 measurements across 248 commodity DDR3 chips show that data-pattern dependence and variable retention time can make a measured deadline context-dependent or stale; the case separates profile persistence from profile correctness, profiling duration from observation of the lowest-retention state, and retained maintenance metadata from payload; see [`evidence/93-dram-1987-2013-vrt-profiling-grounding.md`](evidence/93-dram-1987-2013-vrt-profiling-grounding.md)."
text = insert_after_line(text, 'cases/92-dram-rowhammer-access-induced-retention-failure.md', readme_line)
p.write_text(text)

# ROADMAP bridge + refresh-failure axis
p = Path('ROADMAP.md')
text = p.read_text()
roadmap_line = "- [x] DRAM variable retention time / retention-profile staleness — [`cases/93-dram-variable-retention-time-profile-staleness.md`](cases/93-dram-variable-retention-time-profile-staleness.md), grounded by [`evidence/93-dram-1987-2013-vrt-profiling-grounding.md`](evidence/93-dram-1987-2013-vrt-profiling-grounding.md), adds a second-order maintenance regime: RAIDR 2012 makes future refresh timing depend on retained row-profile/bin state, while IBM 1992, Micron's 2002-filed VRT patent, and Liu et al. 2013 establish that actual cell retention can change over time and that profiling is also data-pattern dependent. The case separates profile persistence from profile correctness, address coverage from temporal-state coverage, ordinary temperature scaling from VRT, and VRT/DPD from RowHammer. Exact pre-1987 genealogy, JEDEC/vendor screening and standards, production adaptive profiling, later on-die ECC, and transistor-level defect history remain separate work."
text = insert_after_line(text, 'cases/92-dram-rowhammer-access-induced-retention-failure.md', roadmap_line)
old_refresh = '- [ ] refresh failure — **partially advanced by grounded Case 92**: RowHammer shows that the ordinary recurring refresh schedule can remain present while repeated neighboring-row activation accelerates victim leakage enough to outrun that schedule, creating an additional workload/topology-conditioned restoration obligation; missed ordinary refresh, self-refresh collapse, controller scheduling faults, modern TRR/RFM failures, and standards-specific refresh-management genealogy remain open;'
new_refresh = '- [ ] refresh failure — **partially advanced by grounded Cases 92 and 93**: Case 92 shows that the ordinary recurring refresh schedule can remain present while repeated neighboring-row activation accelerates victim leakage enough to outrun that schedule; Case 93 shows that a controller can faithfully execute a retention-aware schedule while the retained profile authorizing that schedule has become non-conservative because of VRT, DPD, or an incomplete profiling window. Missed ordinary refresh, self-refresh collapse, controller scheduling faults, modern TRR/RFM failures, production adaptive-profiling evidence, and standards-specific refresh-management genealogy remain open;'
if old_refresh in text:
    text = text.replace(old_refresh, new_refresh, 1)
elif new_refresh not in text:
    raise RuntimeError('refresh failure roadmap anchor missing')
p.write_text(text)

# CASE_INDEX ledger, matrix, aggregate and findings
p = Path('CASE_INDEX.md')
text = p.read_text()
ledger_line = "| [DRAM Variable Retention Time: Profile Staleness and Unstable Preservation Deadlines](cases/93-dram-variable-retention-time-profile-staleness.md) | **grounded** | volatile DRAM charge + retention-time profiling + retained row/bin classification + profile-driven refresh + DPD/VRT-dependent profile uncertainty | separate physical retention behavior from the retained profile that governs maintenance; show that preserved profile metadata can become stale and unsafe; distinguish stochastic VRT and data-pattern context from RowHammer and ordinary temperature scaling | [1987–2013 VRT/profiling grounding](evidence/93-dram-1987-2013-vrt-profiling-grounding.md); exact transistor-defect genealogy, JEDEC/vendor screening, production adaptive profiling, later on-die ECC, and DDR4/DDR5 standards remain separate work |"
text = insert_after_line(text, 'cases/92-dram-rowhammer-access-induced-retention-failure.md', ledger_line)

matrix_row = "| DRAM VRT / retention-time profiling | payload charge + profiled row/cell retention class + refresh-policy state + measurement context | ordinary refresh restores charge; controller may reduce work using retained retention-time bins, but DPD/VRT can invalidate a previously safe classification | ordinary activation/read restoration remains DRAM semantics; the bounded case centers on whether the chosen future refresh deadline remains valid | profile/bin metadata can qualify a row for slower refresh only while conservative for the current physical/context state; revalidation or error tolerance may be required | no authorized deletion path; data can be lost because stale maintenance metadata permits too-long a restoration interval | no complete leakage/history trace is retained; a compressed classification survives while hidden physical VRT state or data-pattern context can change |"
text = insert_after_line(text, 'DRAM RowHammer / targeted refresh', matrix_row)

old = 'After ninety-three bounded cases, **all ninety-three cases are now `grounded`.**'
new = 'After ninety-four bounded cases, **all ninety-four cases are now `grounded`.**'
if old not in text and new not in text:
    raise RuntimeError('aggregate sentence missing')
text = text.replace(old, new, 1)

findings = """

### Case 93 — DRAM variable-retention profile findings

1165. **measured retention time ≠ immutable cell property** — a measured value describes a cell under a particular VRT state and measurement context; the same addressed cell can later require a shorter restoration interval.
1166. **profile persistence ≠ profile correctness** — preserving and restoring retention-bin metadata protects its bits, not the continuing truth of the row-to-deadline relation it encodes.
1167. **static retention profile ≠ guaranteed future safe refresh schedule** — a controller can execute exactly the schedule authorized by its profile and still lose data if the profile has ceased to be conservative.
1168. **retention metadata ≠ user payload** — row/bin classification is secondary control state, yet its correctness participates in whether payload charge survives.
1169. **a longer remembered deadline can be more dangerous than a shorter conservative deadline** — stale metadata can suppress restoration the cell now requires rather than merely reducing observability.
1170. **profiling duration ≠ proof that the lowest retention state was observed** — address coverage can be complete while a VRT cell remains in a high-retention state throughout the measurement window.
1171. **guard band ≠ proof against state changes** — a fixed margin only covers the variation envelope it actually bounds; the 2013 observations include >4× retention-state changes and explicitly reject 2× as a universal guarantee.
1172. **test / assembly qualification ≠ final-system retention profile** — lifecycle transitions such as high-temperature assembly can invalidate an earlier classification even when the profile itself is preserved exactly.
1173. **profiling data pattern ≠ neutral context** — measured retention can depend on values stored elsewhere, so a small pattern set need not expose the worst-case row/cell behavior.
1174. **cell-local retention ≠ neighbor-value-independent retention** — DPD makes the safe interval relational to stored-value context without requiring RowHammer-style repeated access.
1175. **DPD ≠ RowHammer** — data-value-dependent coupling/noise during retention profiling and access-induced disturbance from repeated activation are distinct causal regimes despite both making retention relational.
1176. **VRT ≠ ordinary temperature scaling** — predictable temperature dependence can be incorporated into refresh policy, while VRT adds time-varying leakage/retention states that can occur even at constant temperature.
1177. **profile reuse across boot ≠ physical-state continuity** — a saved profile can cross a reboot while the represented device passes through time, temperature, assembly, or hidden VRT-state transitions.
1178. **retention-aware refresh trades maintenance work for retained classification knowledge** — skipping unnecessary refreshes is enabled by storing a more differentiated account of which rows need restoration sooner.
1179. **stale preservation metadata can actively cause failure** — an obsolete control relation can remain authoritative in exactly the direction that omits necessary maintenance.
1180. **maintenance policy may itself require maintenance / revalidation** — once preservation depends on learned deadlines, profiling, guardbanding, online remeasurement, error tolerance, or conservative fallback become second-order retention work.
"""
if '1165. **measured retention time ≠ immutable cell property**' not in text:
    text = text.rstrip() + findings + '\n'
p.write_text(text)

# Validate cross-navigation and aggregate before removing one-shot integration machinery.
for path in ['README.md', 'ROADMAP.md', 'CASE_INDEX.md']:
    t = Path(path).read_text()
    if CASE_PATH not in t:
        raise RuntimeError(f'{path} missing Case 93 navigation')
if EVID_PATH not in Path('README.md').read_text() or EVID_PATH not in Path('ROADMAP.md').read_text() or EVID_PATH not in Path('CASE_INDEX.md').read_text():
    raise RuntimeError('grounding navigation incomplete')
idx = Path('CASE_INDEX.md').read_text()
if 'After ninety-four bounded cases, **all ninety-four cases are now `grounded`.**' not in idx:
    raise RuntimeError('aggregate status not updated')
if '1180. **maintenance policy may itself require maintenance / revalidation**' not in idx:
    raise RuntimeError('findings incomplete')
if idx.find('DRAM VRT / retention-time profiling') > idx.find('## Cross-case findings already supported'):
    raise RuntimeError('comparison row outside matrix')
if new_refresh not in Path('ROADMAP.md').read_text():
    raise RuntimeError('refresh failure roadmap status not updated')

Path('.github/scripts/case93_integrate.py').unlink(missing_ok=True)
Path('.github/workflows/case93-integration.yml').unlink(missing_ok=True)
