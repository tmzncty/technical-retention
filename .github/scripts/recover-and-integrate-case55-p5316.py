from pathlib import Path

workflow = Path('.github/workflows/integrate-case55-p5316-pel.yml')
text = workflow.read_text(encoding='utf-8')
start_marker = "python3 - <<'PY'\n"
end_marker = "\n          PY\n"
if start_marker not in text or end_marker not in text:
    raise SystemExit('embedded integration script markers not found')
body = text.split(start_marker, 1)[1].split(end_marker, 1)[0]
# The failed YAML staging commit left Python control lines indented as part of the
# run block while multiline research text was not YAML-indented. Recover the
# intended Python by stripping the workflow block indent only where present.
body = '\n'.join(line[10:] if line.startswith('          ') else line for line in body.splitlines()) + '\n'
compile(body, '<recovered-case55-integration>', 'exec')
exec(compile(body, '<recovered-case55-integration>', 'exec'), {'__name__': '__main__'})
