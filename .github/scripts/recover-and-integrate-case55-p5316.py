import subprocess

source_commit = '0e50135e4b12c63217f267736a3c481e79a0c8b5'
path = '.github/workflows/integrate-case55-p5316-pel.yml'
text = subprocess.check_output(['git', 'show', f'{source_commit}:{path}'], text=True)
start_marker = "python3 - <<'PY'\n"
end_marker = "\n          PY\n"
if start_marker not in text or end_marker not in text:
    raise SystemExit('embedded integration script markers not found in staging commit')
body = text.split(start_marker, 1)[1].split(end_marker, 1)[0]
body = '\n'.join(line[10:] if line.startswith('          ') else line for line in body.splitlines()) + '\n'
code = compile(body, '<recovered-case55-integration>', 'exec')
exec(code, {'__name__': '__main__'})
