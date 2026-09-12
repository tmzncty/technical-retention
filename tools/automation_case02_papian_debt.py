from pathlib import Path

ROOT = Path('.')
CASE02 = ROOT / 'cases/02-magnetic-core-destructive-read.md'
CASE70 = ROOT / 'cases/70-magnetic-core-half-select-disturbance.md'
ROADMAP = ROOT / 'ROADMAP.md'
EVIDENCE70 = ROOT / 'evidence/70-papian-1952-half-select-disturbance-facsimile-deepening.md'


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected one anchor, found {count}: {old[:120]!r}')
    path.write_text(text.replace(old, new, 1), encoding='utf-8')


if not EVIDENCE70.exists():
    raise SystemExit('Case-70 Papian direct-facsimile evidence is missing; refusing reconciliation')

ev = EVIDENCE70.read_text(encoding='utf-8')
required = [
    'direct inspection of William N. Papian',
    'pulse amplitude',
    'pulse length',
    'spacing',
    'number of intervening nonselecting pulses',
    'The direct-facsimile debt for Papian 1952 is closed',
]
for needle in required:
    if needle not in ev:
        raise SystemExit(f'Case-70 evidence no longer contains expected grounding text: {needle!r}')

# 1) Give Case 02 an explicit link to the already-completed direct-facsimile work.
case02 = CASE02.read_text(encoding='utf-8')
link_line = ('Papian direct-facsimile deepening: '
             '[`../evidence/70-papian-1952-half-select-disturbance-facsimile-deepening.md`]'
             '(../evidence/70-papian-1952-half-select-disturbance-facsimile-deepening.md). '
             'This Case-70 record supplies the page-level 1952 IRE inspection that Case 02 previously carried as archival cleanup; '
             'its quantitative disturbance analysis remains scoped to Case 70 rather than being duplicated here.')
if link_line not in case02:
    anchor = ('Power-transition retention deepening: '
              '[`../evidence/02-1965-1966-core-power-transition-retention-deepening.md`]'
              '(../evidence/02-1965-1966-core-power-transition-retention-deepening.md). '
              'This later IBM/DEC machine evidence grounds `unpowered retention != transition immunity != whole-machine restart continuity`; '
              "it does not replace the case's 1950–1954 MIT anchor.")
    if case02.count(anchor) != 1:
        raise SystemExit('Case 02 top navigation anchor missing or duplicated')
    case02 = case02.replace(anchor, anchor + '\n\n' + link_line, 1)

old_cleanup = ('Remaining archival cleanup is narrower: obtain a conveniently renderable full scan of Papian\'s 1952 IRE paper for direct page-level inspection. '
               'The central Case-02 claims no longer depend uniquely on its abstract.')
new_cleanup = ('The former Papian-1952 facsimile cleanup is now **closed** by the direct inspection recorded in '
               '[`../evidence/70-papian-1952-half-select-disturbance-facsimile-deepening.md`]'
               '(../evidence/70-papian-1952-half-select-disturbance-facsimile-deepening.md). '
               'Case 02 therefore no longer carries a page-level Papian evidence debt. '
               'Further work is narrower and belongs mainly to Case 70 or `computing-archaeology`: named-machine quantitative half-select/current/sense margins, '
               'production material distributions, temperature dependence, exact correspondence between Papian test materials and deployed arrays, and broader invention-priority genealogy.')
if old_cleanup in case02:
    case02 = case02.replace(old_cleanup, new_cleanup, 1)
elif new_cleanup not in case02:
    raise SystemExit('Case 02 archival-cleanup anchor missing and replacement not already present')

old_note = ('Papian\'s 1952 IRE paper remains contemporary technical evidence for remanence and repeated nonselecting disturbances; '
            'direct page-level inspection of a conveniently renderable full scan remains archival cleanup. '
            'The case no longer depends uniquely on that abstract because the grounding record adds Papian\'s 1953 implemented-memory paper, Mayer & Papian M-2121, and other primary witnesses.')
new_note = ('Papian\'s 1952 IRE paper remains contemporary technical evidence for remanence and repeated nonselecting disturbances. '
            'Direct page-level inspection is now recorded in the Case-70 facsimile deepening, which independently grounds the pulse-pattern variables and disturbed-signal boundaries without forcing Case 02 to duplicate the narrower half-select analysis. '
            'Case 02 also remains independently grounded by Papian\'s 1953 implemented-memory paper, Mayer & Papian M-2121, and other primary witnesses.')
if old_note in case02:
    case02 = case02.replace(old_note, new_note, 1)
elif new_note not in case02:
    raise SystemExit('Case 02 source-note anchor missing and replacement not already present')
CASE02.write_text(case02, encoding='utf-8')

# 2) Make Case 70 explicitly own the quantitative follow-up and record that it closes Case 02's stale archival debt.
case70 = CASE70.read_text(encoding='utf-8')
old70 = ('The original grounding used MIT\'s preserved abstract to establish repeated `nonselecting` disturbance as a retention criterion. '
         'Direct inspection of the article facsimile now closes that evidence debt; see '
         '[`../evidence/70-papian-1952-half-select-disturbance-facsimile-deepening.md`]'
         '(../evidence/70-papian-1952-half-select-disturbance-facsimile-deepening.md).')
new70 = (old70 + '\n\nThe same direct facsimile also closes the older Case-02 roadmap/source-note request for page-level inspection of the 1952 IRE paper. '
         'Case 02 keeps the general remanence + destructive-read + rewrite argument; Case 70 owns the narrower quantitative half-select/disturbed-signal analysis, so the two cases share evidence without duplicating scope.')
if old70 in case70 and 'closes the older Case-02 roadmap/source-note request' not in case70:
    case70 = case70.replace(old70, new70, 1)
elif 'closes the older Case-02 roadmap/source-note request' not in case70:
    raise SystemExit('Case 70 direct-facsimile anchor missing')
CASE70.write_text(case70, encoding='utf-8')

# 3) Reconcile ROADMAP so it no longer asks for work already completed under Case 70.
old_roadmap = ('Remaining archival cleanup: obtain a directly renderable full scan of Papian\'s 1952 IRE paper; central claims no longer depend uniquely on it.')
new_roadmap = ('[x] **Papian 1952 direct-facsimile cleanup closed via Case 70:** '
               '[`evidence/70-papian-1952-half-select-disturbance-facsimile-deepening.md`]'
               '(evidence/70-papian-1952-half-select-disturbance-facsimile-deepening.md) now supplies page-level inspection of the IRE paper, '
               'including repeated half-amplitude nonselecting-pulse test geometry, independently variable pulse amplitude/length/spacing/count, and disturbed-signal discrimination. '
               'Case 02 now links rather than duplicates that narrower analysis. Remaining magnetic-core work is production/named-machine quantitative margin evidence, temperature/material distributions, and broader genealogy, primarily under Case 70 / `computing-archaeology`.')
replace_once(ROADMAP, old_roadmap, new_roadmap)
