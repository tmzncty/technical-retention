from pathlib import Path

p = Path('evidence/44-nvme12-13-deallocate-sanitize-grounding.md')
text = p.read_text(encoding='utf-8')
old_title = '# Case 44 Grounding — NVMe Deallocate and Sanitize (2016–2017)'
new_title = '# Case 44 Grounding — TCG Opal / NVMe Deallocate and Sanitize (2009–2017)'
if text.count(old_title) != 1:
    raise SystemExit('unexpected Case 44 grounding title state')
text = text.replace(old_title, new_title, 1)
old_purpose = 'This record grounds [`../cases/44-nvme13-deallocate-sanitize-forgetting.md`](../cases/44-nvme13-deallocate-sanitize-forgetting.md) in official NVM Express Revision 1.3 and Revision 1.2.1 text. It records the exact evidence needed to keep four different relations apart:'
new_purpose = 'This record grounds [`../cases/44-nvme13-deallocate-sanitize-forgetting.md`](../cases/44-nvme13-deallocate-sanitize-forgetting.md) in official TCG Opal 1.0 Revision 1.0 plus NVM Express Revision 1.3 and Revision 1.2.1 text. It records the exact evidence needed to keep deallocation, physical erasure, cryptographic key retirement, and completed subsystem sanitization from collapsing into one generic `erase` relation:'
if text.count(old_purpose) != 1:
    raise SystemExit('unexpected Case 44 grounding purpose state')
text = text.replace(old_purpose, new_purpose, 1)
p.write_text(text.rstrip() + '\n', encoding='utf-8')
