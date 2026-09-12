import subprocess

workflow_path = '.github/workflows/automation-case55-pm9a3.yml'
start_marker = "          python3 - <<'PY'\n"
end_marker = "\n          PY\n"

refs = subprocess.check_output(['git', 'rev-list', '--max-count=20', 'HEAD'], text=True).splitlines()
raw = None
source_ref = None
for ref in refs:
    try:
        candidate = subprocess.check_output(['git', 'show', f'{ref}:{workflow_path}'], text=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        continue
    if start_marker in candidate and end_marker in candidate:
        raw = candidate
        source_ref = ref
        break
if raw is None:
    raise SystemExit('Could not find ancestor workflow containing embedded Case 55 Python payload')

start = raw.index(start_marker) + len(start_marker)
end = raw.index(end_marker, start)
code_lines = raw[start:end].splitlines()
code = '\n'.join(line[10:] if line.startswith('          ') else line for line in code_lines) + '\n'
compile(code, f'<case55-payload-from-{source_ref}>', 'exec')
exec(code, {'__name__': '__main__'})
