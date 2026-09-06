from pathlib import Path

INDEX_PATH = Path('CASE_INDEX.md')
index = INDEX_PATH.read_text(encoding='utf-8')
if '## Case 102 — Dell PERC / LSI MegaRAID Patrol Read findings' in index:
    raise SystemExit('CASE_INDEX already contains Case 102 findings')

lines = index.splitlines()
try:
    cross_idx = lines.index('## Cross-case findings already supported')
except ValueError:
    raise SystemExit('Could not locate cross-case findings boundary')

# Case 101 was grounded in the previous slice but its integration script only
# appended findings and ROADMAP state. Repair that missing Cases-table navigation
# row while adding Case 102, so CASE_INDEX remains authoritative.
last_case_row = None
for i in range(cross_idx - 1, -1, -1):
    if lines[i].startswith('| [') and '](' in lines[i] and 'cases/' in lines[i]:
        last_case_row = i
        break
if last_case_row is None:
    raise SystemExit('Could not locate final case-table row')

row101 = '| [SCSI Background Medium Scan: Proactive Readability Verification, Defect Logging, and Conditional Reassignment](cases/101-scsi-background-medium-scan-proactive-defect-discovery.md) | **grounded** | device-side proactive medium-readability scan + retained defect/progress evidence + ARRE/AWRE-conditioned remediation | separate latent-defect discovery, logging, repair permission, reassignment, and payload preservation; keep device-side BMS distinct from higher-layer scrub/Patrol Read | [2004–2007 T10/Seagate grounding record](evidence/101-t10-2004-2007-background-medium-scan-grounding.md); host SCSI VERIFY and broader controller genealogy remain open |'
row102 = '| [Dell PERC / LSI MegaRAID Patrol Read: Media Verification Versus RAID Consistency Checking](cases/102-perc-megaraid-patrol-read-consistency-boundary.md) | **grounded** | controller-driven proactive physical-media verification + separate RAID redundancy consistency checking + bad-block remediation / optional reconstruction | separate media readability from parity consistency, maintenance scheduling from coverage proof, and repair capability from repair outcome without inventing a BMS/Patrol-Read genealogy | [2005–2009 Dell/LSI grounding record](evidence/102-dell-lsi-2005-2009-patrol-read-grounding.md); host SCSI VERIFY, cross-vendor controller genealogy, exact firmware lineage, and fault injection remain open |'

insert_rows = []
if not any('cases/101-scsi-background-medium-scan-proactive-defect-discovery.md' in line for line in lines[:cross_idx]):
    insert_rows.append(row101)
if not any('cases/102-perc-megaraid-patrol-read-consistency-boundary.md' in line for line in lines[:cross_idx]):
    insert_rows.append(row102)
if not insert_rows:
    raise SystemExit('Expected at least Case 102 table row to be absent')
lines[last_case_row + 1:last_case_row + 1] = insert_rows

index = '\n'.join(lines).rstrip('\n')
last = index.splitlines()[-1]
if not last.startswith('1518. **BMS standardization ≠ invention of background scanning'):
    raise SystemExit(f'Unexpected CASE_INDEX tail before Case 102: {last[:160]}')

findings = r'''

## Case 102 — Dell PERC / LSI MegaRAID Patrol Read findings

1519. **physical-media verification ≠ redundancy-consistency verification** — Dell explicitly separates Patrol Read's physical-disk/media-defect role from Consistency Check's data/parity validation role;
1520. **RAID-controller Patrol Read ≠ drive-internal Background Medium Scan** — both can proactively exercise media before demand, but Case 101 locates BMS inside the SCSI device server while Case 102 locates Patrol Read at the RAID-controller maintenance layer;
1521. **physical-drive maintenance scope ≠ redundant virtual-drive consistency scope** — later MegaRAID documentation allows Patrol Read across drives/hot spares and all RAID levels, while Consistency Check is defined for redundant virtual drives;
1522. **task distinction ≠ disjoint error coverage** — Dell Consistency Check can also encounter bad blocks, and later MegaRAID events show medium-error outcomes under both task families;
1523. **correctable medium error ≠ uncorrectable medium error** — later controller event vocabulary preserves separate outcomes rather than one generic bad-sector state;
1524. **bad-block handling / puncture ≠ successful payload restoration** — a controller can record or isolate a defective location without thereby proving that the logical data was reconstructed and restored;
1525. **Patrol Read completion ≠ parity-consistency certification** — completing a physical-media scan does not establish that redundant data/parity relations have been checked by Consistency Check;
1526. **Consistency Check completion ≠ controller-wide media-coverage certification** — validating redundant virtual-drive relations does not establish recent Patrol Read coverage of every physical scope such as hot spares or system-reserved areas;
1527. **automatic patrol schedule ≠ maintenance-free persistence** — automatic mode retains recurring maintenance policy, but continued verification still consumes controller time and competes with foreground/background work;
1528. **maintenance event/progress state ≠ user payload state** — controller logs/status retain evidence about scans, errors, and corrections without being the data whose retention is at issue;
1529. **named PERC feature introduction ≠ invention of background disk verification** — Dell can date introduction of `Background Patrol Read` to bounded PERC firmware/driver families without establishing priority over earlier proprietary, host, or device-side scanning;
1530. **shared `Patrol Read` terminology/function ≠ proven controller genealogy** — Dell PERC and later LSI MegaRAID material can be compared historically and functionally, but shared naming does not by itself prove firmware descent or OEM implementation identity;
1531. **media readability ≠ parity consistency ≠ end-to-end checksum integrity** — PERC/MegaRAID media checks, RAID consistency checks, and higher-layer ZFS-style checksum authority qualify different relations even when each is called proactive integrity maintenance.
'''
INDEX_PATH.write_text(index + findings.rstrip('\n') + '\n', encoding='utf-8')

text = INDEX_PATH.read_text(encoding='utf-8')
if 'cases/101-scsi-background-medium-scan-proactive-defect-discovery.md' not in text:
    raise SystemExit('Case 101 table-navigation repair missing')
if 'cases/102-perc-megaraid-patrol-read-consistency-boundary.md' not in text:
    raise SystemExit('Case 102 table-navigation row missing')
if '1531. **media readability ≠ parity consistency ≠ end-to-end checksum integrity**' not in text:
    raise SystemExit('Case 102 findings missing')
print('case102 CASE_INDEX finalized')
