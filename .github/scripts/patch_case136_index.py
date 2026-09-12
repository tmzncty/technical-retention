from pathlib import Path

index = Path('CASE_INDEX.md')
text = index.read_text(encoding='utf-8')
assert '- **3603 —' in text, 'expected previous final finding 3603'
assert '- **3604 —' not in text, 'finding 3604 already exists'

section = '''## Case 136 — Dell PERC surviving-source unreadability / RAID-puncture deepening findings

Deepening record: [`evidence/136-dell-2013-2018-perc-puncture-source-readability-deepening.md`](evidence/136-dell-2013-2018-perc-puncture-source-readability-deepening.md).

- **3604 — March 2013 PERC rebuild can complete with errors:** Dell OpenManage documentation for named PERC 4 controllers says a rebuild can complete successfully while reporting errors and can restore healthy portions but not a damaged portion. (`H/P`)
- **3605 — degraded-state media damage can cross a recoverability boundary:** the 2013 guide says medium/bad-block damage discovered during rebuild or degraded operation can leave damaged data unrecoverable from the virtual disk without restoration from backup. (`H/P`)
- **3606 — Dell explicitly names RAID puncture / rebuild with errors:** the November 2018 PowerEdge troubleshooting guide defines RAID puncture as PERC behavior that can let rebuild continue when a double fault exceeds the impacted stripe's redundancy. (`H/P`)
- **3607 — one failed member plus one surviving same-stripe data error can defeat RAID 5 reconstruction:** Dell's worked example says insufficient information remains for that stripe, which is lost/punctured during rebuild. (`H/P`)
- **3608 — restored redundancy can coexist with lost payload:** the 2018 guide says puncturing can restore redundancy and return the array to an optimal state while the affected stripe remains lost. (`H/P`)
- **3609 — post-puncture Check Consistency is not recovery:** Dell says Check Consistency after a RAID puncture is induced does not resolve it, and recommends proactive Check Consistency, especially before drive replacement when possible. (`H/P`)
- **3610 — rebuild progress/completion != reconstructable coverage:** global rebuild can continue after a local stripe becomes unreconstructable and is punctured. (`E`)
- **3611 — array optimal / redundancy restored != complete payload integrity:** restored redundancy after puncture does not retroactively recover the lost stripe. (`E`)
- **3612 — rebuild rate / repair priority != source readability:** surviving-source readability/reconstructability is a constitutive repair input independent of scheduling resources. (`E`)
- **3613 — latent surviving-source defect != second whole-device failure:** either can remove a contribution required by a degraded stripe, but they differ in scope and failure object. (`E`)
- **3614 — proactive integrity/readability maintenance can preserve future repair opportunity:** discovering latent defects before another member loss consumes redundancy margin is functionally comparable to Cases 18/101/102, without mechanism identity. (`E/A`)
- **3615 — RAID 5 puncture geometry is not universal RAID geometry:** Case 94 RAID 6 provides a code-margin counterexample, so Dell's RAID 5 example is not generalized to dual parity. (`A`)
- **3616 — faster repair does not certify readable sources:** Case 96 / faster-repair comparison is limited to exposure time; higher rebuild priority or shorter rebuild does not by itself prevent puncture. (`A`)
- **3617 — puncture is not sanitization:** loss of a logical stripe does not establish forensic erasure of prior physical embodiments. (`X`, rejected upgrade)
- **3618 — Dell manuals establish documentation floors, not invention priority:** the 2013/2018 records do not prove first use of puncture terminology or identical firmware genealogy across PERC generations. (`X`, rejected upgrade)
- **3619 — no universal URE-risk model is inferred:** vendor manuals do not establish a universal URE probability, failure rate, correlation model, or quantitative rebuild-risk curve; cross-vendor evidence and fault injection remain open. (`X`, scope boundary)
'''

index.write_text(text.rstrip() + '\n\n' + section, encoding='utf-8')

# Validate the partial integration produced before the main helper's known CASE_INDEX-schema assertion.
case = Path('cases/136-megaraid-perc-rebuild-rate-repair-priority.md').read_text(encoding='utf-8')
roadmap = Path('ROADMAP.md').read_text(encoding='utf-8')
assert 'Surviving-source readability can limit reconstruction even while rebuild continues' in case
assert '136-dell-2013-2018-perc-puncture-source-readability-deepening.md' in case
assert 'Case 136 deepening — Dell PERC surviving-source unreadability' in roadmap
assert Path('evidence/136-dell-2013-2018-perc-puncture-source-readability-deepening.md').exists()
final = index.read_text(encoding='utf-8')
for fid in range(3604, 3620):
    assert f'- **{fid} —' in final, fid
