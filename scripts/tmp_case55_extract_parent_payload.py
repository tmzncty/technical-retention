from pathlib import Path
import subprocess

workflow_path = '.github/workflows/automation-case55-pm9a3.yml'
raw = subprocess.check_output(['git', 'show', f'HEAD^:{workflow_path}'], text=True)
start_marker = "          python3 - <<'PY'\n"
end_marker = "\n          PY\n"
start = raw.index(start_marker) + len(start_marker)
end = raw.index(end_marker, start)
code_lines = raw[start:end].splitlines()
# The invalid workflow kept Python statement lines at ten-space YAML indentation,
# while multiline string payload lines were flush-left. Strip only that YAML
# indentation so the extracted Python becomes executable without modifying the
# payload text itself.
code = '\n'.join(line[10:] if line.startswith('          ') else line for line in code_lines) + '\n'
compile(code, '<case55-parent-payload>', 'exec')
exec(code, {'__name__': '__main__'})
