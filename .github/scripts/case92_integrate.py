from pathlib import Path

CASE_PATH = 'cases/92-dram-rowhammer-access-induced-retention-failure.md'
EVID_PATH = 'evidence/92-dram-2012-2014-rowhammer-grounding.md'


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
readme_line = "- [`cases/92-dram-rowhammer-access-induced-retention-failure.md`](cases/92-dram-rowhammer-access-induced-retention-failure.md) — grounded DRAM disturbance bridge: 2014 commodity-DDR3 measurements show that repeated activation of one aggressor row can accelerate charge leakage in physically nearby victim rows inside the ordinary refresh window, while Intel's 2012-filed row-hammer patent supplies an earlier industry witness for thresholded activity detection and targeted victim-row refresh; the case separates ordinary refresh compliance from disturbance immunity, logical addressing from physical interference topology, and global periodic refresh from workload-conditioned restoration; see [`evidence/92-dram-2012-2014-rowhammer-grounding.md`](evidence/92-dram-2012-2014-rowhammer-grounding.md)."
text = insert_after_line(text, 'cases/91-apache-cassandra-tombstone-grace-zombie-prevention.md', readme_line)
p.write_text(text)

# ROADMAP bridge + refresh-failure axis
p = Path('ROADMAP.md')
text = p.read_text()
roadmap_line = "- [x] DRAM RowHammer / access-induced retention failure — [`cases/92-dram-rowhammer-access-induced-retention-failure.md`](cases/92-dram-rowhammer-access-induced-retention-failure.md), grounded by [`evidence/92-dram-2012-2014-rowhammer-grounding.md`](evidence/92-dram-2012-2014-rowhammer-grounding.md), adds an interference-conditioned DRAM regime beyond ordinary deadline refresh: Kim et al. 2014 experimentally show repeated aggressor-row activation accelerating nearby victim-cell charge loss inside the ordinary refresh interval, while Intel's 2012-filed targeted-refresh patent supplies an earlier industry witness for thresholded row-hammer detection and victim-row refresh. The case separates ordinary refresh compliance from disturbance immunity, weak-retention cells from disturbance victims, logical row identity from physical adjacency, and global faster refresh from access/topology-conditioned maintenance. Exact pre-2012 disturbance genealogy, JEDEC/vendor TRR/RFM evolution, later bypasses, and security-exploit history remain separate work."
text = insert_after_line(text, 'cases/91-apache-cassandra-tombstone-grace-zombie-prevention.md', roadmap_line)
old_refresh = '- [ ] refresh failure;'
new_refresh = '- [ ] refresh failure — **partially advanced by grounded Case 92**: RowHammer shows that the ordinary recurring refresh schedule can remain present while repeated neighboring-row activation accelerates victim leakage enough to outrun that schedule, creating an additional workload/topology-conditioned restoration obligation; missed ordinary refresh, self-refresh collapse, controller scheduling faults, modern TRR/RFM failures, and standards-specific refresh-management genealogy remain open;'
if old_refresh in text:
    text = text.replace(old_refresh, new_refresh, 1)
elif new_refresh not in text:
    raise RuntimeError('refresh failure roadmap anchor missing')
p.write_text(text)

# CASE_INDEX ledger, matrix, aggregate and findings
p = Path('CASE_INDEX.md')
text = p.read_text()
ledger_line = "| [DRAM RowHammer: Access-Induced Retention Failure and Targeted Refresh](cases/92-dram-rowhammer-access-induced-retention-failure.md) | **grounded** | volatile DRAM charge + ordinary periodic refresh + access-induced neighbor leakage + aggressor/victim topology + optional access-threshold/targeted-refresh state | separate scheduled-refresh compliance from disturbance immunity; logical isolation from physical electrical isolation; weak-retention cells from disturbance victims; global periodic refresh from access/topology-conditioned restoration | [2012–2014 RowHammer grounding](evidence/92-dram-2012-2014-rowhammer-grounding.md); exact pre-2012 disturbance genealogy, JEDEC/vendor TRR/RFM evolution, modern bypasses, stronger ECC interaction, and exploit history remain separate work |"
text = insert_after_line(text, 'cases/91-apache-cassandra-tombstone-grace-zombie-prevention.md', ledger_line)

matrix_row = "| DRAM RowHammer / targeted refresh | victim-cell charge + ordinary refresh cadence + aggressor/victim relation + optional access-count/threshold state + physical-adjacency mapping | ordinary timed refresh restores charge; repeated aggressor activation can accelerate victim leakage; stronger global refresh or targeted neighbor refresh adds workload/topology-conditioned maintenance | row activation restores the opened aggressor yet can indirectly endanger neighboring victims; once a victim value has corrupted, refresh alone is not evidence of original-payload reconstruction | refresh cadence plus disturbance-mitigation policy qualify reliability; physical adjacency/mapping knowledge matters for selective victim refresh | no authorized deletion path in the bounded case; a bit flip is unintended state change, not deliberate forgetting | no complete access history is required by PARA; counter-based alternatives retain bounded activity/threshold state rather than a full trace |"
text = insert_after_line(text, 'Apache Cassandra tombstone grace / compaction purge', matrix_row)

old = 'After ninety-two bounded cases, **all ninety-two cases are now `grounded`.**'
new = 'After ninety-three bounded cases, **all ninety-three cases are now `grounded`.**'
if old not in text and new not in text:
    raise RuntimeError('aggregate sentence missing')
text = text.replace(old, new, 1)

findings = """

### Case 92 — DRAM RowHammer findings

1149. **ordinary refresh compliance ≠ disturbance immunity** — the recurring DRAM refresh schedule can still be present while sufficiently frequent aggressor-row activation makes victim cells lose charge inside that ordinary window.
1150. **time-driven leakage ≠ access-induced accelerated leakage** — both reduce charge margin, but RowHammer adds activity in another row as a rate-changing causal variable rather than merely extending time since restoration.
1151. **own-row access ≠ only-own-row physical effect** — a requested activation targets one row logically while repeated wordline activity can alter the retention conditions of physically nearby non-target rows.
1152. **logical address isolation ≠ physical electrical isolation** — distinct row addresses do not by themselves guarantee that the underlying cells are free of interference coupling.
1153. **victim cell ≠ ordinary weak-retention cell** — the 2014 characterization found little overlap between disturbance victims and cells identified as weak by a long no-refresh/no-access retention test in the examined modules.
1154. **aggressor restoration can coexist with victim degradation** — repeatedly opening the aggressor restores that row's own charge while contributing to accelerated leakage in victim rows.
1155. **retention interval can be workload- and topology-conditioned** — under coupling, how long a victim remains safely recoverable depends partly on neighboring physical activity, not elapsed time alone.
1156. **global faster refresh ≠ targeted refresh** — increasing periodic refresh for every row and refreshing only rows threatened by detected/inferred aggressor activity use different triggers, scope, retained control state, and cost.
1157. **targeted refresh ≠ payload correction after corruption** — renewing a still-correct victim's charge margin is preventative maintenance; the inspected sources do not establish refresh alone as reconstruction of an already-flipped original value.
1158. **ECC presence ≠ failsafe against multi-bit disturbance** — the measured multi-victim patterns can exceed ordinary SECDED correction/detection assumptions in some 64-bit words.
1159. **logical row adjacency ≠ guaranteed physical adjacency** — manufacturer mapping/remapping can make the physical interference neighborhood differ from the obvious logical numbering.
1160. **topology knowledge can become retention infrastructure** — selective victim preservation requires some component to resolve a hammered row into the physical rows whose charge margin is endangered.
1161. **access-history tracking ≠ complete access-history retention** — counter/threshold mitigations can keep only bounded activity state sufficient for a maintenance decision rather than every access event.
1162. **PARA statelessness ≠ absence of maintenance policy** — the proposal removes per-row counter/address history yet still couples a probabilistic neighbor-refresh rule to row-close events.
1163. **2014 RowHammer measurements ≠ universal device threshold** — 139K and related observations belong to the tested modules; later generations, vendors, mappings, and mitigations require their own evidence.
1164. **interference makes retention relational** — a local bit's continued recoverability can depend on operations performed on another physical structure, so retention cannot always be modeled as an isolated bearer plus a clock.
"""
if '1149. **ordinary refresh compliance ≠ disturbance immunity**' not in text:
    text = text.rstrip() + findings + '\n'
p.write_text(text)

# Validate cross-navigation and aggregate before removing one-shot integration machinery.
for path in ['README.md', 'ROADMAP.md', 'CASE_INDEX.md']:
    t = Path(path).read_text()
    if CASE_PATH not in t:
        raise RuntimeError(f'{path} missing Case 92 navigation')
if EVID_PATH not in Path('README.md').read_text() or EVID_PATH not in Path('ROADMAP.md').read_text() or EVID_PATH not in Path('CASE_INDEX.md').read_text():
    raise RuntimeError('grounding navigation incomplete')
idx = Path('CASE_INDEX.md').read_text()
if 'After ninety-three bounded cases, **all ninety-three cases are now `grounded`.**' not in idx:
    raise RuntimeError('aggregate status not updated')
if '1164. **interference makes retention relational**' not in idx:
    raise RuntimeError('findings incomplete')
if idx.find('DRAM RowHammer / targeted refresh') > idx.find('## Cross-case findings already supported'):
    raise RuntimeError('comparison row outside matrix')
if new_refresh not in Path('ROADMAP.md').read_text():
    raise RuntimeError('refresh failure roadmap status not updated')

Path('.github/scripts/case92_integrate.py').unlink(missing_ok=True)
Path('.github/workflows/case92-integration.yml').unlink(missing_ok=True)
