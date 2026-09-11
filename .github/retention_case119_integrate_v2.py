from pathlib import Path

case_path = Path('cases/119-ddr4-post-package-repair-row-remapping.md')
roadmap_path = Path('ROADMAP.md')
index_path = Path('CASE_INDEX.md')
evidence_rel = 'evidence/119-micron-ddr4-ppr-payload-retention-resource-exhaustion-deepening.md'
evidence_path = Path(evidence_rel)
assert evidence_path.exists(), evidence_path

case = case_path.read_text()
old_grounding = 'Grounding record: [`../evidence/119-ddr4-1979-2023-post-package-repair-grounding.md`](../evidence/119-ddr4-1979-2023-post-package-repair-grounding.md).'
new_grounding = 'Grounding records: [`../evidence/119-ddr4-1979-2023-post-package-repair-grounding.md`](../evidence/119-ddr4-1979-2023-post-package-repair-grounding.md) + [`../evidence/119-micron-ddr4-ppr-payload-retention-resource-exhaustion-deepening.md`](../evidence/119-micron-ddr4-ppr-payload-retention-resource-exhaustion-deepening.md).'
if old_grounding in case:
    case = case.replace(old_grounding, new_grounding, 1)
else:
    assert new_grounding in case

section = '''## Payload-retention and repair-resource deepening

Micron's DDR4 PPR sequence documentation closes two evidence debts left by the original grounding; see [`../evidence/119-micron-ddr4-ppr-payload-retention-resource-exhaustion-deepening.md`](../evidence/119-micron-ddr4-ppr-payload-retention-resource-exhaustion-deepening.md).

First, **persistent row repair does not by itself define payload preservation across the repair transition**. In Micron's documented `sPPR` path, the bank is expected to retain array data except for the seed row and associated row addresses; if those contents must survive the repair, they are explicitly backed up before sPPR and restored afterwards. Micron's `hPPR` documentation likewise exposes two command-sequence envelopes: one supports data retention under its stated refresh conditions, while the other does not support data retention for the target DRAM.

Second, **repair support does not imply that a repair resource is still available**. Micron states that once the hPPR resource for a bank is used up, the bank should be treated as lacking sPPR resources as well; a repair sequence issued when no repair resource is available is ignored.

The engineering reconstruction can therefore be sharpened to:

```text
logical row-address continuity
!=
repair-mapping persistence
!=
payload preservation across repair

PPR capability
!=
repair resource available now

repair sequence issued
!=
new repair mapping installed
```

For the bounded sPPR path, data-preserving maintenance is a compound workflow:

```text
back up affected seed / associated rows
    -> perform repair/remap transition
    -> restore payload
```

That is not evidence for a universal DDR4 migration algorithm. It is evidence that **mapping continuity and payload continuity are distinct obligations even inside one vendor's documented PPR procedure**.

Repair-resource exhaustion also makes future maintainability stateful: consuming a finite repair resource changes which later defect-repair transitions remain admissible. This is a repository-level engineering reconstruction, not Micron's historical terminology and not a claim that every DDR4 vendor exposes the same spare topology or count.

Finally, none of these transitions establishes sanitization. Backing up/restoring data, redirecting a row address, retiring a defective row, or consuming a spare does not prove that data remaining in the old physical embodiment has been securely erased or made forensically inaccessible.

---

'''
if '## Payload-retention and repair-resource deepening' not in case:
    marker = '\n---\n\n## Historical record\n'
    assert case.count(marker) == 1
    case = case.replace(marker, '\n---\n\n' + section + '## Historical record\n', 1)

repls = {
    '- establish exact target-row data-preservation/destruction semantics for each PPR sequence and product;': '- extend the now-grounded Micron target-row/associated-row preservation semantics to JEDEC text and Samsung/SK hynix products before making any cross-vendor rule;',
    '- characterize repair-resource exhaustion and telemetry on named DIMMs;': '- characterize physical repair-resource topology/counts, exhaustion telemetry, and success/failure reporting on named DIMMs without projecting the bounded Micron behavior across vendors;',
}
for old, new in repls.items():
    if old in case:
        case = case.replace(old, new, 1)
    else:
        assert new in case, old
case_path.write_text(case)

roadmap = roadmap_path.read_text()
roadmap_bullet = '''- [x] **Case 119 deepening — DDR4 PPR payload-preservation / finite repair-resource boundary** — [`cases/119-ddr4-post-package-repair-row-remapping.md`](cases/119-ddr4-post-package-repair-row-remapping.md), deepened by [`evidence/119-micron-ddr4-ppr-payload-retention-resource-exhaustion-deepening.md`](evidence/119-micron-ddr4-ppr-payload-retention-resource-exhaustion-deepening.md): Micron DDR4 product documentation grounds that sPPR payload preservation can require explicit seed/associated-row backup and post-repair restoration; hPPR exposes command-sequence variants with different data-retention envelopes; and a PPR sequence issued to a bank with no repair resource available is ignored. This closes the bounded `persistent remap != automatic payload preservation`, `PPR capability != currently available repair resource`, and `repair sequence issued != repair mapping changed` seams. Cross-vendor resource topology/counts, exact JEDEC adoption chronology, named-platform completion telemetry, and physical post-repair characterization remain open; row retirement/remapping is not treated as sanitization. `computing-archaeology` was rechecked and has no dedicated PPR module to reuse.
'''
if 'Case 119 deepening — DDR4 PPR payload-preservation' not in roadmap:
    marker = '### Recent bounded evidence deepening\n\n'
    assert roadmap.count(marker) == 1
    roadmap = roadmap.replace(marker, marker + roadmap_bullet, 1)
phase_line_old = 'target-row payload semantics, repair-resource exhaustion, and fault injection remain open.'
phase_line_new = 'cross-vendor target-row payload semantics, physical repair-resource topology/exhaustion telemetry, and fault injection remain open.'
if phase_line_old in roadmap:
    roadmap = roadmap.replace(phase_line_old, phase_line_new, 1)
else:
    assert phase_line_new in roadmap
roadmap_path.write_text(roadmap)

idx = index_path.read_text()
lines = idx.splitlines()
row_matches = [i for i, line in enumerate(lines) if '(cases/119-ddr4-post-package-repair-row-remapping.md)' in line]
assert len(row_matches) == 1, row_matches
ri = row_matches[0]
if '119-micron-ddr4-ppr-payload-retention-resource-exhaustion-deepening.md' not in lines[ri]:
    anchor = '[1979–2023 grounding record](evidence/119-ddr4-1979-2023-post-package-repair-grounding.md)'
    extra = ' + [Micron payload-retention / repair-resource deepening](evidence/119-micron-ddr4-ppr-payload-retention-resource-exhaustion-deepening.md)'
    if anchor in lines[ri]:
        lines[ri] = lines[ri].replace(anchor, anchor + extra, 1)
    else:
        pos = lines[ri].rfind(' |')
        assert pos > 0
        lines[ri] = lines[ri][:pos] + '; ' + extra.lstrip(' +') + lines[ri][pos:]
idx = '\n'.join(lines) + ('\n' if idx.endswith('\n') else '')

findings = '''
- **3496 — H/P:** Micron's 16Gb DDR4 `sPPR Row Repair` documentation states that the repaired bank is expected to retain array data except for the seed row and its associated row addresses, making the preservation exception explicit rather than treating PPR as a transparent whole-bank copy.
- **3497 — H/P:** When the seed/associated-row data must be retained across sPPR, Micron instructs that those rows be backed up before the repair and restored after sPPR completes; payload continuity is therefore a documented operation surrounding the remap transition.
- **3498 — H/P:** Micron states that when the hPPR resource for a bank is used up, that bank should be assumed not to have resources available for sPPR, exposing a finite bank-scoped maintenance-capacity boundary in the documented family.
- **3499 — H/P:** Micron further states that a repair sequence issued to a bank with no repair resource available is ignored; issuing the sequence is therefore not itself evidence that a new repair mapping was established.
- **3500 — H/P:** Micron's hPPR documentation exposes two command-sequence forms with different payload-retention envelopes: a `WRA`-based sequence supports data retention under its stated refresh conditions, while a `WR`-based sequence does not support data retention for the target DRAM.
- **3501 — E:** `persistent repair mapping != payload preservation across the repair transition`; the address-to-spare relation and the data carried through maintenance are separate retained obligations.
- **3502 — E:** For the bounded Micron sPPR path, data-preserving maintenance is a compound protocol — backup affected seed/associated rows, perform the repair/remap transition, then restore payload — rather than one indivisible remap operation.
- **3503 — E:** `PPR capability != repair resource currently available`; a device may implement the PPR interface while a particular bank has exhausted the resource needed for another repair.
- **3504 — E:** `repair sequence issued != repair-state transition`; the documented no-resource path is an explicit counterexample because the programming sequence is ignored.
- **3505 — E:** Remaining repair capacity is second-order retention infrastructure: consuming it changes which future defect-repair transitions remain admissible even though the resource is not ordinary user payload.
- **3506 — A:** Case 14 SCSI defect reassignment is a bounded functional comparison because both preserve an address relation across physical substitution while payload continuity remains a separate question; disk defect mapping and DDR4 row PPR are not the same mechanism or genealogy.
- **3507 — A:** Case 04 mapped Flash and spare-block/sector exhaustion are only abstract comparisons for `finite hidden maintenance capacity constrains future repair`; Flash erase/program/reclamation geometry is not projected onto DRAM PPR.
- **3508 — I:** Project interpretation only: maintainability itself can have retained state, because the future ability to preserve logical identity through another substitution depends on unconsumed repair capacity. This is not Micron's historical vocabulary.
- **3509 — X:** Backing up/restoring rows, retiring a defective row, consuming a spare, or installing a persistent hPPR relation does not establish sanitization, overwrite, or forensic inaccessibility of the retired physical row.
- **3510 — X:** No universal DDR4 spare-row count, repair-resource topology, fuse/antifuse mechanism, or cross-vendor exhaustion rule is inferred from the bounded Micron product documentation.
- **3511 — X:** No claim is made that all hPPR preserves payload, that all hPPR destroys payload, or that this deepening establishes the first JEDEC revision/ballot to introduce hPPR/sPPR; those remain product- and chronology-specific evidence questions.
'''
if '**3496 — H/P:**' not in idx:
    assert '**3495 — X:**' in idx, 'expected current finding 3495 missing'
    idx = idx.rstrip() + '\n' + findings + '\n'
index_path.write_text(idx)

for path in (case_path, roadmap_path, index_path, evidence_path):
    assert path.exists() and path.stat().st_size > 0, path
print('Case 119 PPR payload/resource integration prepared')
