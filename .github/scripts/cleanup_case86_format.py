from pathlib import Path

fixes = {
    'cases/02-magnetic-core-destructive-read.md': [
        (
            'while volatile execution/control state still requires a separate save, reset, and restart protocol;\n\n- [`tmzncty/problem-history`',
            'while volatile execution/control state still requires a separate save, reset, and restart protocol;\n- [`tmzncty/problem-history`',
        ),
    ],
    'evidence/86-dec-1960-1970-core-power-restart-grounding.md': [
        (
            '| controlled shutdown preservation ≠ failure-triggered automatic restart | IBM 1968 + DEC 1966 | E | strong bounded comparison | no lineage/circuit equivalence claim |\n\n| core-content survival ≠ execution-context survival |',
            '| controlled shutdown preservation ≠ failure-triggered automatic restart | IBM 1968 + DEC 1966 | E | strong bounded comparison | no lineage/circuit equivalence claim |\n| core-content survival ≠ execution-context survival |',
        ),
        (
            '- `processor continuation ≠ peripheral/external-world continuity`.\n- `controlled power-transition preservation ≠ arbitrary-failure restart`;',
            '- `processor continuation ≠ peripheral/external-world continuity`;\n- `controlled power-transition preservation ≠ arbitrary-failure restart`;',
        ),
    ],
}

for path, replacements in fixes.items():
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    for old, new in replacements:
        if new in text:
            continue
        if old not in text:
            raise SystemExit(f'format anchor missing in {path}: {old[:120]!r}')
        text = text.replace(old, new, 1)
    p.write_text(text, encoding='utf-8')

print('Case 02 / Case 86 markdown formatting cleanup applied.')
