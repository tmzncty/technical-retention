from pathlib import Path

CASE_PATH = 'cases/123-ata6-device-configuration-overlay-capability-retention.md'
EVIDENCE_PATH = 'evidence/123-ata-2000-2007-dco-grounding.md'

roadmap = Path('ROADMAP.md')
text = roadmap.read_text(encoding='utf-8')
case123 = "- [x] ATA/ATAPI-6 Device Configuration Overlay / persistent capability-configuration boundary — [`cases/123-ata6-device-configuration-overlay-capability-retention.md`](cases/123-ata6-device-configuration-overlay-capability-retention.md), grounded by [`evidence/123-ata-2000-2007-dco-grounding.md`](evidence/123-ata-2000-2007-dco-grounding.md): T13 records the e00140 DCO proposal series in July–October 2000 and INCITS 361-2002 / ATA/ATAPI-6 in the following standards generation; a 2003 Maxtor DiamondMax Plus9 manual supplies a named shipping-product witness, while later ATA8-ACS working-draft continuity makes the retained-state boundary explicit: DCO can reduce commands, modes, feature sets, and capacity; a reduced maximum changes READ NATIVE MAX itself; DCO SET state survives power-on/hardware reset; and DCO FREEZE LOCK has a distinct power-cycle-bounded authority lifetime. This closes only the bounded `selectable capability baseline vs current advertised surface vs DCO-modified capacity vs configuration lifetime vs lock lifetime` relation; final ATA/ATAPI-6 facsimile inspection, proposal-text archaeology, OEM/BIOS deployment, independent drive traces, forensic media validation, and broader ATA configuration genealogy remain open."
lines = text.splitlines()
anchor_i = next(i for i, line in enumerate(lines) if line.startswith('- [x] ATA/ATAPI-4 Host Protected Area / SET MAX'))
if not any(CASE_PATH in line for line in lines):
    lines.insert(anchor_i, case123)
    anchor_i += 1
lines[anchor_i] = lines[anchor_i].replace(
    'final-standard facsimile comparison, DCO, PARTIES/BIOS history,',
    'final-standard facsimile comparison, PARTIES/BIOS history,'
)
continuation = 'DCO capability/configuration layering is now handled separately by grounded Case 123.'
if continuation not in lines[anchor_i]:
    lines[anchor_i] += ' ' + continuation
roadmap.write_text('\n'.join(lines) + '\n', encoding='utf-8')

idx = Path('CASE_INDEX.md')
text = idx.read_text(encoding='utf-8')
lines = text.splitlines()
row = "| [ATA/ATAPI-6 Device Configuration Overlay: Persistent Capability Reduction Beneath the HPA Frontier](cases/123-ata6-device-configuration-overlay-capability-retention.md) | **grounded** | selectable factory/capability baseline + persistent reduced DCO configuration + current ordinary IDENTIFY surface + DCO-modified maximum capacity + power-cycle-bounded DCO freeze-lock authority | separate current advertised support from selectable support; HPA-native maximum from DCO factory/selectable maximum; configuration persistence from authority-lock lifetime; and interface restoration from payload validation/forgetting | [2000–2007 DCO grounding](evidence/123-ata-2000-2007-dco-grounding.md); final ATA/ATAPI-6 facsimile, proposal-text archaeology, OEM/BIOS deployment, independent drive traces, and forensic validation remain open |"
if not any(CASE_PATH in line for line in lines):
    anchor_i = next(i for i, line in enumerate(lines) if 'cases/122-ata4-host-protected-area-addressability-retention.md' in line)
    lines.insert(anchor_i + 1, row)
text = '\n'.join(lines) + '\n'

findings = '''

## Case 123 — ATA Device Configuration Overlay capability-retention findings

- **1982 — 18 July 2000 DCO proposal record ≠ invention date:** T13's e00140r0/r1/r2 metadata establishes a public standards-development floor, not private conception or absolute mechanism priority. (`H/P`, `X`)
- **1983 — ATA/ATAPI-6 standards record ≠ inspected final normative facsimile:** T13 lists INCITS 361-2002, while exact mechanism wording in this slice is recovered from later ATA8-ACS continuity and a 2003 product manual; final ATA/ATAPI-6 clause comparison remains evidence debt. (`H/P`, `X`)
- **1984 — current ordinary capability report ≠ selectable DCO baseline:** after DCO SET, ordinary IDENTIFY may report a reduced command/mode/feature/capacity surface while DCO IDENTIFY retains the selectable baseline. (`H/P`, `E`)
- **1985 — reported unsupported ≠ demonstrated physical impossibility:** DCO can require the device not to provide a configured-out feature while DCO IDENTIFY still records it as selectable; interface absence alone does not prove hardware impossibility. (`H/P`, `E`, `X`)
- **1986 — DCO capacity reduction changes READ NATIVE MAX itself:** the later ATA contract explicitly makes DCO maximum-LBA changes modify READ NATIVE MAX / EXT results. (`H/P`)
- **1987 — READ NATIVE MAX ≠ universal factory-capacity oracle:** Case 122's HPA-native observation remains conditioned by the deeper DCO configuration regime. (`H/P`, `E`, `X`)
- **1988 — HPA current frontier ≠ DCO selectable/factory capacity baseline:** HPA can lower ordinary reach below READ NATIVE MAX, while DCO can lower the maximum that READ NATIVE MAX reports. (`H/P`, `A`)
- **1989 — payload persistence ≠ capability-configuration persistence:** DCO retains a service/configuration relation across power/reset without thereby changing the magnetic retention mechanism of user sectors. (`H/P`, `E`)
- **1990 — successful DCO SET ≠ one-session configuration:** the bounded later contract says power-on or hardware reset does not change DCO SET settings and returns a configured device to Reduced_config. (`H/P`)
- **1991 — persistent reduced configuration ≠ DCO FREEZE LOCK lifetime:** the freeze blocks DCO management through hardware/software reset only until the subsequent power-on reset, while the reduced configuration can survive that power-on transition. (`H/P`, `E`)
- **1992 — authority-state expiry ≠ configuration rollback:** ending the DCO freeze window at power-on restores the ability to issue management commands; it does not by itself restore Factory_config. (`H/P`, `E`)
- **1993 — DCO RESTORE ≠ payload restoration:** RESTORE re-enables configured-out capabilities and ordinary reporting when allowed; it does not reconstruct or validate sector contents. (`H/P`, `E`, `X`)
- **1994 — DCO-hidden/inaccessible capacity ≠ deallocation ≠ sanitization:** capability/capacity withdrawal does not specify overwrite, erase, key destruction, or another secure-forgetting operation. (`H/P`, `A`, `X`)
- **1995 — DCO and HPA coexistence ≠ independent composition:** DCO SET/RESTORE validity rules explicitly depend on whether an HPA is established, so the two addressability-control state machines can constrain one another. (`H/P`, `E`)
- **1996 — one device capacity ≠ one observer-independent number:** ordinary IDENTIFY, READ NATIVE MAX, and DCO IDENTIFY can answer differently because each is qualified by a different configuration/view relation. (`H/P`, `E`)
- **1997 — Case 113 encoding capability ≠ Case 123 configuration-authorized capability:** enough address bits to represent an LBA or a selectable 48-bit feature does not by itself mean the current DCO surface exposes that capability. (`A`)
- **1998 — Case 89 address representation ≠ Case 123 capability overlay:** CHS/LBA translation changes designation representation; DCO changes which commands/features/capacity the current interface contract provides. (`A`)
- **1999 — 2003 Maxtor product witness ≠ universal implementation behavior:** DiamondMax Plus9 proves one named ATA/ATAPI-6-era family exposed the DCO command set and support bits, not first implementation, universal conformance, or hidden-sector integrity. (`H/P`, `X`)
- **2000 — related-repository boundary:** current `tmzncty/computing-archaeology` searches found no dedicated DCO case; broad ATA configuration/HPA/DCO/BIOS genealogy belongs there if developed, while Case 123 retains only the capability/configuration-lifetime relation. (`H/P` project-state record)
'''
if '## Case 123 — ATA Device Configuration Overlay capability-retention findings' not in text:
    text = text.rstrip() + findings + '\n'
idx.write_text(text, encoding='utf-8')

c122 = Path('cases/122-ata4-host-protected-area-addressability-retention.md')
text = c122.read_text(encoding='utf-8')
text = text.replace(
    '- a Device Configuration Overlay (`DCO`) case;',
    '- a Device Configuration Overlay (`DCO`) case; that follow-on is now grounded separately as [Case 123](123-ata6-device-configuration-overlay-capability-retention.md);'
)
text = text.replace(
    '- DCO can also alter visible capacity in later ATA generations but is a separate mechanism and remains outside this slice.',
    '- DCO can also alter visible capacity and even the `READ NATIVE MAX` observation in later ATA generations; that separate capability/configuration layer is now grounded in [Case 123](123-ata6-device-configuration-overlay-capability-retention.md).'
)
c122.write_text(text, encoding='utf-8')
