from pathlib import Path

ROOT = Path('.')


def insert_after_line(text: str, predicate, new_line: str, label: str) -> str:
    lines = text.splitlines()
    if new_line in lines:
        return text
    for i, line in enumerate(lines):
        if predicate(line):
            lines.insert(i + 1, new_line)
            return '\n'.join(lines) + ('\n' if text.endswith('\n') else '')
    raise RuntimeError(f'anchor not found: {label}')


def replace_prefixed_line(text: str, prefix: str, new_line: str, label: str) -> str:
    lines = text.splitlines()
    hits = [i for i, line in enumerate(lines) if line.startswith(prefix)]
    if len(hits) != 1:
        raise RuntimeError(f'expected one {label} line, found {len(hits)}')
    lines[hits[0]] = new_line
    return '\n'.join(lines) + ('\n' if text.endswith('\n') else '')


# README navigation
p = ROOT / 'README.md'
text = p.read_text()
readme_case = "- [`cases/89-ata-lba-chs-translation-logical-sector-identity.md`](cases/89-ata-lba-chs-translation-logical-sector-identity.md) — grounded ATA logical-addressing bridge: ATA-2/ATA-3 keep a logical sector's LBA invariant across mutable logical-CHS translation, separately report current CHS capacity and total LBA-addressable sectors, and a 1997 SyQuest EIDE manual explicitly says logical sector address does not imply actual physical media location; see [`evidence/89-ata-1994-1997-lba-chs-translation-grounding.md`](evidence/89-ata-1994-1997-lba-chs-translation-grounding.md)."
text = insert_after_line(
    text,
    lambda line: line.startswith('- [`cases/88-linux-md-raid5-partial-parity-log.md`]'),
    readme_case,
    'README Case 88',
)
readme_evidence = "- [`evidence/89-ata-1994-1997-lba-chs-translation-grounding.md`](evidence/89-ata-1994-1997-lba-chs-translation-grounding.md) — Case-89 grounding record: ATA-2/ATA-3 standards text plus SyQuest's 1997 commercial EIDE manual separate stable LBA designation, mutable logical-CHS presentation, current-CHS versus total-LBA reachability, and actual physical media location without turning address translation into defect remapping, payload relocation, secure erasure, or an ATA invention-priority claim."
text = insert_after_line(
    text,
    lambda line: line.startswith('- [`evidence/88-linux-1993-2017-raid5-ppl-grounding.md`]'),
    readme_evidence,
    'README evidence 88',
)
p.write_text(text)


# ROADMAP: add bounded completed slice and deepen the broad HDD line while keeping it open.
p = ROOT / 'ROADMAP.md'
text = p.read_text()
road_case = "- [x] ATA-2 / ATA-3 logical-CHS translation and LBA-invariance bridge — [`cases/89-ata-lba-chs-translation-logical-sector-identity.md`](cases/89-ata-lba-chs-translation-logical-sector-identity.md), grounded by [`evidence/89-ata-1994-1997-lba-chs-translation-grounding.md`](evidence/89-ata-1994-1997-lba-chs-translation-grounding.md), separates a stable logical-sector LBA from mutable CHS translation parameters, current CHS reach from the total LBA-addressable set, and logical geometry from actual media position. ATA-3's `orphan sectors` show that one addressing regime can lose reach without proving sector absence, while SyQuest's 1997 manual explicitly denies a necessary logical-address/physical-location relation. This is a bounded retention/address-identity slice, not a complete CHS→LBA chronology or an FTL genealogy."
text = insert_after_line(
    text,
    lambda line: line.startswith('- [x] Linux MD RAID5 Partial Parity Log / write-hole recovery-evidence boundary'),
    road_case,
    'ROADMAP Case 88 completed slice',
)
road_hdd = "- [ ] HDD geometry, bad-sector remapping, CHS → LBA — **partially advanced by grounded bounded Cases 14 and 89**: [`cases/14-scsi-disk-defect-reassignment-logical-identity.md`](cases/14-scsi-disk-defect-reassignment-logical-identity.md) uses 1990–1997 period-primary evidence to separate host LBA from physical target, manufacturer-defect slipping from grown-defect replacement, defect metadata from payload, and successful physical reassignment from payload preservation. [`cases/89-ata-lba-chs-translation-logical-sector-identity.md`](cases/89-ata-lba-chs-translation-logical-sector-identity.md), grounded by [`evidence/89-ata-1994-1997-lba-chs-translation-grounding.md`](evidence/89-ata-1994-1997-lba-chs-translation-grounding.md), now adds the ATA translation axis: one logical sector keeps the same LBA across current logical-CHS translations; `IDENTIFY DEVICE` separates current CHS capacity from total LBA capacity; ATA-3 names CHS-unreachable/LBA-reachable `orphan sectors`; and SyQuest explicitly says logical sector address does not imply actual media location. The broad item stays unchecked because physical recording geometry, zone-bit recording, early SCSI/IDE/ATA genealogy, BIOS translation/capacity barriers, LBA28→LBA48, controller implementation history, and named-drive physical-layout validation remain separate work best developed in `computing-archaeology`."
text = replace_prefixed_line(text, '- [ ] HDD geometry, bad-sector remapping, CHS → LBA —', road_hdd, 'ROADMAP HDD broad item')
p.write_text(text)


# CASE_INDEX ledger, matrix, aggregate, findings.
p = ROOT / 'CASE_INDEX.md'
text = p.read_text()
ledger = "| [ATA LBA / CHS Translation: Logical-Sector Identity Across Geometry Representation](cases/89-ata-lba-chs-translation-logical-sector-identity.md) | **grounded** | magnetic-disk logical sectors + stable LBA designation + mutable logical-CHS translation parameters + separately hidden physical media placement | separate LBA continuity from CHS-coordinate continuity; logical geometry from physical geometry; current-CHS reachability from total LBA reachability; and translation change from physical relocation/defect reassignment | [1994–1997 ATA translation grounding](evidence/89-ata-1994-1997-lba-chs-translation-grounding.md); full CHS→LBA/BIOS/ATA genealogy, actual zoned platter geometry, LBA48 evolution, and named-drive physical mapping remain separate work |"
text = insert_after_line(
    text,
    lambda line: line.startswith('| [Linux MD RAID5 Partial Parity Log: Retaining Just Enough Recovery Evidence'),
    ledger,
    'CASE_INDEX Case 88 ledger row',
)
matrix = "| ATA logical CHS/LBA translation / 1994–1997 bounded regime | user payload on magnetic media + stable logical-sector LBA + current/default logical-CHS translation parameters + capacity descriptors | no refresh-like retention work is established; host/controller may re-parameterize CHS presentation while normal device machinery resolves logical sectors to hidden media positions | host can select CHS or LBA for supported media commands; the same logical sector keeps its LBA across CHS translation changes | LBA is linear logical designation; CHS tuple depends on current heads/sectors translation; SyQuest says neither logical address implies actual physical media position | logical designation can remain stable while CHS coordinate changes; Case 14 separately shows physical serving sector can also change under defect reassignment | no complete address-history retention: current/default translation state is enough for presentation, while stable LBA identity does not require preserving every prior CHS tuple |"
text = insert_after_line(
    text,
    lambda line: line.startswith('| Linux MD RAID5 PPL / 2017 bounded regime |'),
    matrix,
    'CASE_INDEX Case 88 matrix row',
)
text = text.replace('After eighty-nine bounded cases,', 'After ninety bounded cases,')
text = text.replace('Cases 00–88', 'Cases 00–89')
text = text.replace('89 grounded cases', '90 grounded cases')

findings = r'''

## Case 89 — ATA LBA / CHS translation findings

1101. **stable LBA ≠ stable CHS tuple** — ATA-2 explicitly keeps a logical sector's LBA unchanged while current logical-CHS translation parameters can change the cylinder/head/sector tuple used to represent it;
1102. **logical CHS ≠ actual physical media location** — SyQuest's 1997 EIDE manual directly states that logical sector addresses have no implied relationship to the sector's actual physical location on the medium;
1103. **translation change ≠ payload relocation** — `INITIALIZE DEVICE PARAMETERS` changes the logical CHS presentation; the bounded command semantics do not establish that user sectors are physically moved merely because heads/sectors translation changes;
1104. **current CHS capacity ≠ total LBA-addressable capacity** — ATA-3 reports current logical-CHS capacity separately from the total LBA sector count, and states that the LBA total does not depend on current device geometry;
1105. **CHS-unreachable ≠ logically absent** — ATA-3's `orphan sectors` can lie beyond the current CHS-addressable range while remaining within the device's LBA-addressable sector set;
1106. **addressing-mode choice ≠ different payload population** — an LBA-capable ATA device can select current CHS translation or LBA per command, so syntax/coordinate regime alone does not imply a different stored value;
1107. **current translation state ≠ user payload** — current heads/sectors/cylinders are interface/control state used to interpret CHS requests rather than the sector data being retained;
1108. **reset/default translation recovery ≠ payload reset** — ATA-3 distinguishes current values derived from the last translation command from default/reset values, so presentation-state reinitialization must not be equated with erasing or recreating user sectors;
1109. **stable LBA ≠ payload-integrity guarantee** — address identity can survive even when magnetic media later become unreadable; the translation rule is not an ECC, scrub, or recovery guarantee;
1110. **stable LBA ≠ stable physical sector** — Case 89 removes the CHS-coordinate inference, while Case 14 independently shows defect reassignment can change the physical medium serving the same LBA;
1111. **representational remapping ≠ defect remapping** — changing logical CHS parameters and substituting a spare physical sector are different mechanisms even though both can preserve an upper logical designation;
1112. **ATA translation ≠ Flash Translation Layer** — Case 04's mapped Flash performs erase-constrained relocation/currentness/reclamation work; ATA CHS/LBA translation is only a bounded functional comparison about designation abstraction;
1113. **geometry-shaped syntax ≠ exposed platter geometry** — the presence of cylinder/head/sector fields in a host interface does not prove the host is naming literal current platter coordinates;
1114. **coordinate continuity ≠ identity continuity** — Case 89 adds a middle layer to the repository's location argument: the same retained logical object can outlive not only a physical embodiment but also one coordinate representation of that embodiment;
1115. **coexisting CHS and LBA support ≠ one clean historical replacement event** — ATA-2/ATA-3 and the 1997 SparQ witness support both modes, so the bounded evidence rejects a simplistic instantaneous `CHS was replaced by LBA` chronology;
1116. **ATA-2/ATA-3/SyQuest evidence ≠ invention-priority proof** — Case 14 already supplies earlier/parallel LBA-versus-physical-target evidence, and the broader SCSI/IDE/BIOS/ATA genealogy remains a separate history.
'''
if '## Case 89 — ATA LBA / CHS translation findings' not in text:
    text = text.rstrip() + findings + '\n'
p.write_text(text)


# Validate all permanent files and state before self-removal.
for required in [
    'cases/89-ata-lba-chs-translation-logical-sector-identity.md',
    'evidence/89-ata-1994-1997-lba-chs-translation-grounding.md',
]:
    if not (ROOT / required).exists():
        raise RuntimeError(f'missing required file: {required}')

checks = {
    'README.md': ['cases/89-ata-lba-chs-translation-logical-sector-identity.md', 'evidence/89-ata-1994-1997-lba-chs-translation-grounding.md'],
    'ROADMAP.md': ['ATA-2 / ATA-3 logical-CHS translation and LBA-invariance bridge', 'Cases 14 and 89'],
    'CASE_INDEX.md': ['cases/89-ata-lba-chs-translation-logical-sector-identity.md', '| ATA logical CHS/LBA translation / 1994–1997 bounded regime |', '1101. **stable LBA ≠ stable CHS tuple**', '1116. **ATA-2/ATA-3/SyQuest evidence ≠ invention-priority proof**', 'After ninety bounded cases,'],
}
for fn, needles in checks.items():
    body = (ROOT / fn).read_text()
    for needle in needles:
        if needle not in body:
            raise RuntimeError(f'{fn}: missing {needle}')

# One-shot cleanup: remove integration machinery from the final tree.
(Path('.github/scripts/case89_integrate.py')).unlink(missing_ok=True)
(Path('.github/workflows/case89-integrate.yml')).unlink(missing_ok=True)
