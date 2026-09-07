from pathlib import Path

paths = [
    Path('cases/115-apache-hdfs-snapshot-shared-block-replication.md'),
    Path('evidence/115-hadoop-2012-2014-snapshot-shared-block-grounding.md'),
]

for path in paths:
    text = path.read_text()
    if text.startswith('\\\n'):
        text = text[2:]
    if text.startswith('\\\r\n'):
        text = text[3:]
    path.write_text(text)
