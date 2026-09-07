from pathlib import Path
import re
import subprocess

ROADMAP = Path('ROADMAP.md')
INDEX = Path('CASE_INDEX.md')

case_path = 'cases/114-nvme14-namespace-write-protection.md'
evidence_path = 'evidence/114-nvme-1996-2019-namespace-write-protection-grounding.md'
assert Path(case_path).exists(), case_path
assert Path(evidence_path).exists(), evidence_path

roadmap = ROADMAP.read_text(encoding='utf-8')
roadmap_marker = '## Phase 2 — Build missing technical bridges\n\n'
roadmap_item = (
    '- [x] NVMe 1.4 Namespace Write Protection / mutation-authority persistence boundary — '
    '[`cases/114-nvme14-namespace-write-protection.md`](cases/114-nvme14-namespace-write-protection.md), grounded by '
    '[`evidence/114-nvme-1996-2019-namespace-write-protection-grounding.md`](evidence/114-nvme-1996-2019-namespace-write-protection-grounding.md): '
    'the 2019 revision-1.4 contract separates namespace payload retention from retained write authority, defines distinct reset/power-cycle lifetimes for ordinary, temporary-until-power-cycle, and permanent protection states, and requires namespace-associated volatile write-cache data/metadata to reach nonvolatile media as part of transition into protection. A 10 May 1996 X3T10 SSC proposal supplies an earlier persistent/permanent software write-protect vocabulary/mechanism floor without proving SCSI→NVMe genealogy. This closes only the bounded `payload persistence vs mutation authority vs transition durability vs authority lifetime` relation; TP4005c archaeology, final SSC genealogy, RPMB provisioning, named-controller conformance, crash/power-cycle fault tests, NVMe-oF/virtualization behavior, and physical/forensic media effects remain open.\n'
)
if case_path not in roadmap:
    assert roadmap_marker in roadmap
    roadmap = roadmap.replace(roadmap_marker, roadmap_marker + roadmap_item, 1)
ROADMAP.write_text(roadmap, encoding='utf-8')

index = INDEX.read_text(encoding='utf-8')
row = (
    '| [NVM Express 1.4 Namespace Write Protection: Mutation Authority, State Lifetime, and Transition Durability]'
    '(cases/114-nvme14-namespace-write-protection.md) | **grounded** | namespace payload + volatile write-cache state + per-namespace write-protection state + capability/authentication state + reset/power-cycle lifetime | '
    'separate payload nonvolatility, durability closure, mutation authority, Feature saveability, authority-state lifetime, health read-only state, and physical WORM; show protection entry can require cache-to-NVM closure while later reads remain admissible | '
    '[1996–2019 grounding record](evidence/114-nvme-1996-2019-namespace-write-protection-grounding.md); TP4005c/revision genealogy, final SSC lineage, RPMB provisioning, named-controller conformance, crash/power-cycle fault validation, NVMe-oF/virtualization behavior, and physical/forensic media effects remain open |\n'
)
if case_path not in index:
    lines = index.splitlines(keepends=True)
    matches = [i for i, line in enumerate(lines) if 'cases/113-ata-atapi6-48bit-lba-reachability.md' in line]
    assert len(matches) == 1, matches
    lines.insert(matches[0] + 1, row)
    index = ''.join(lines)

findings_heading = '## Case 114 — NVMe 1.4 Namespace Write Protection findings'
findings = r'''

## Case 114 — NVMe 1.4 Namespace Write Protection findings

- **1781 — namespace write-protection state ≠ payload-retention physics:** NVMe 1.4 can prohibit host-visible mutation of an otherwise nonvolatile namespace without changing NAND charge-retention time, ECC margin, or proving physical immobility. (`H/P`, `E`)
- **1782 — write protected ≠ unreadable:** the bounded command-interaction table allows Read and other nonmodifying operations while rejecting actions that modify the protected namespace medium. (`H/P`)
- **1783 — write protection ≠ deletion or sanitization:** blocking Format/Sanitize-style modification authority does not itself deallocate, erase, cryptographically erase, or physically sanitize the namespace payload. (`H/P`, `E`)
- **1784 — Feature Identifier `not saveable` ≠ protection state volatile:** Feature 84h is not saveable through the generic Feature-save mechanism, yet most namespace write-protection states persist across both power cycles and Controller Level Resets. (`H/P`)
- **1785 — `Write Protect Until Power Cycle` ≠ reset-temporary protection:** the state survives an NVMe Controller Level Reset and clears only on the specified power-cycle transition. (`H/P`)
- **1786 — ordinary `Write Protect` ≠ `Permanent Write Protect`:** both survive power cycles/resets in the bounded 1.4 state table, but they have different transition/changeability semantics. (`H/P`)
- **1787 — `Permanent Write Protect` ≠ physically WORM medium:** protocol-level permanence constrains the defined host/controller mutation path; the specification does not establish physically write-once NAND, indefinite media retention, or immutable lower-layer embodiment. (`H/P`, `E`, `X`)
- **1788 — shared namespace attachment ≠ independent per-controller protection authority:** if the subsystem supports Namespace Write Protection, the namespace state must be enforced by every controller to which that namespace is attached. (`H/P`)
- **1789 — protection entry ≠ metadata-only bit flip:** a Set Features transition into a protected state requires all volatile write-cache data and metadata associated with that namespace to be committed to nonvolatile media as part of the transition. (`H/P`)
- **1790 — transition durability closure ≠ future mutation prohibition:** the cache-to-NVM transfer closes outstanding volatile state; the protected state then constrains future modifying commands. NVMe 1.4 composes these operations without making them the same relation. (`H/P`, `E`)
- **1791 — deliberate namespace read-only state ≠ media-health read-only warning:** §8.19.1 says the Critical Warning read-only condition is not set merely because namespace write protection made the namespace read-only. (`H/P`)
- **1792 — capability existence ≠ transition authorization:** support for Namespace Write Protection and the current protection state are distinct from RPMB-based authentication control governing transitions into `Write Protect Until Power Cycle` and `Permanent Write Protect`. (`H/P`)
- **1793 — 2019 NVMe feature ≠ invention of persistent/permanent software write protection:** X3T10/96-179r0 (10 May 1996) already proposes `Persistent Write Protect` and `Permanent Write Protect` for SSC volumes across mounts. (`H/P` prior-art floor)
- **1794 — 1996 SSC prior art ≠ proven SCSI→NVMe genealogy:** the SSC proposal is tape-volume/device-server specific and proposes medium-recorded protection indication; NVMe 1.4 uses a namespace/controller feature with different state, attachment, authentication, and transition semantics. (`H/P`, `A`, `X`)
- **1795 — Case 110 service-level WORM ≠ Case 114 namespace-level protocol write protection:** S3 Object Lock is version-scoped with retain-until/legal-hold/Governance/Compliance relations; NVMe 1.4 is namespace-scoped with reset/power-cycle/permanent state lifetimes. The comparison is functional only. (`A`)
- **1796 — related-repository boundary:** `tmzncty/computing-archaeology` has no dedicated Namespace Write Protection case to reuse in this round; broader SCSI/ATA/NVMe write-protection genealogy and controller history should be developed there rather than duplicated here. (`H/P` project-state record)
'''
if findings_heading not in index:
    nums = [int(x) for x in re.findall(r'\*\*(\d+)\s+—', index)]
    assert nums and max(nums) == 1780, max(nums) if nums else None
    index = index.rstrip() + findings + '\n'

INDEX.write_text(index, encoding='utf-8')

# Basic consistency checks.
text = INDEX.read_text(encoding='utf-8')
assert text.count(case_path) == 1
assert text.count(findings_heading) == 1
assert '**1796 — related-repository boundary:**' in text
road = ROADMAP.read_text(encoding='utf-8')
assert road.count('[`cases/114-nvme14-namespace-write-protection.md`]') == 1

subprocess.run(['git', 'diff', '--check'], check=True)
subprocess.run(['git', 'config', 'user.name', 'Tmzncty'], check=True)
subprocess.run(['git', 'config', 'user.email', '72063145+tmzncty@users.noreply.github.com'], check=True)
subprocess.run(['git', 'add', 'ROADMAP.md', 'CASE_INDEX.md'], check=True)
subprocess.run(['git', 'rm', '-f', '.case114_integrate.py'], check=True)
subprocess.run(['git', 'commit', '-m', 'case114: integrate NVMe write-protection navigation'], check=True)
subprocess.run(['git', 'push', 'origin', 'main'], check=True)
