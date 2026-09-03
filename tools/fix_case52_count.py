from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "CASE_INDEX.md"
WORKFLOW = ROOT / ".github/workflows/fix-case52-count.yml"
SCRIPT = ROOT / "tools/fix_case52_count.py"

text = INDEX.read_text()
old = "currently fifty-two;"
new = "currently fifty-three;"
if old in text:
    if text.count(old) != 1:
        raise RuntimeError(f"unexpected stale-count multiplicity: {text.count(old)}")
    text = text.replace(old, new, 1)
elif new not in text:
    raise RuntimeError("expected synthesis-gate count phrase not found")

if "After fifty-three bounded cases, **all fifty-three cases are now `grounded`.**" not in text:
    raise RuntimeError("main Case 52 status count is missing")
if "515. **successful selected-page read" not in text or "527. **commercial-chip characterization" not in text:
    raise RuntimeError("Case 52 findings are missing")
INDEX.write_text(text)

if WORKFLOW.exists():
    WORKFLOW.unlink()
if SCRIPT.exists():
    SCRIPT.unlink()

subprocess.run(["git", "config", "user.name", "github-actions[bot]"], cwd=ROOT, check=True)
subprocess.run(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], cwd=ROOT, check=True)
subprocess.run(["git", "add", "CASE_INDEX.md", ".github/workflows/fix-case52-count.yml", "tools/fix_case52_count.py"], cwd=ROOT, check=True)
subprocess.run(["git", "diff", "--cached", "--check"], cwd=ROOT, check=True)
if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode != 0:
    subprocess.run(["git", "commit", "-m", "docs: reconcile Case 52 synthesis count"], cwd=ROOT, check=True)
    subprocess.run(["git", "push", "origin", "HEAD:main"], cwd=ROOT, check=True)
