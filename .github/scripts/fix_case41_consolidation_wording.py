from pathlib import Path

repls = {
    Path('cases/41-apache-cassandra-tombstone-gc-grace-resurrection.md'): {
        'A separate later-added Case 41 repeated most of the same tombstone / grace / resurrection mechanism while adding useful older evidence.':
        'A separate later-added duplicate case repeated most of the same tombstone / grace / resurrection mechanism while adding useful older evidence.'
    },
    Path('evidence/41-cassandra-3x-tombstone-repair-grounding.md'): {
        'This section absorbs the unique evidence from the now-consolidated later Case 41.':
        'This section absorbs the unique evidence from the now-consolidated duplicate case.'
    },
}

for path, mapping in repls.items():
    text = path.read_text()
    for old, new in mapping.items():
        assert old in text, f'missing expected wording in {path}: {old}'
        text = text.replace(old, new, 1)
    path.write_text(text)

for path in repls:
    text = path.read_text()
    assert 'later-added Case 41 repeated' not in text
    assert 'now-consolidated later Case 41' not in text

print('Case 41 consolidation wording fixed.')
