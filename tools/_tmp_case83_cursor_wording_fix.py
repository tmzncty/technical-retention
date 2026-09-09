from pathlib import Path
import subprocess

p = Path('cases/83-apache-hdfs-block-scanner-checksum-verification.md')
text = p.read_text(encoding='utf-8')
old = "`VolumeScanner` periodically calls `saveBlockIterator`. Its scheduling code explicitly explains why the iterator records **wall-clock** time in a `cursor file`: monotonic time commonly resets on machine reboot, while the persisted cursor must survive that boundary. The code saves the iterator at the end of a block-pool pass and contains a configured-interval save branch during a pass."
new = "`VolumeScanner` has explicit `saveBlockIterator` paths and a configured in-pass save branch. Its scheduling code explains why the iterator records **wall-clock** time in a `cursor file`: monotonic time commonly resets on machine reboot, while the persisted cursor must survive that boundary. The code saves the iterator at the end of a block-pool pass and on orderly scanner exit, while the configured-interval branch is intended to checkpoint during a pass."
if text.count(old) != 1:
    raise SystemExit(f'expected one target paragraph, found {text.count(old)}')
text = text.replace(old, new, 1)
p.write_text(text.rstrip() + '\n', encoding='utf-8')
subprocess.run(['git', 'diff', '--check'], check=True)
print('Case 83 cursor wording corrected')
