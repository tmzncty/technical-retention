from pathlib import Path

CASE = Path('cases/76-jedec-ssd-endurance-retention-qualification.md')
EVIDENCE = Path('evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md')
ROADMAP = Path('ROADMAP.md')
INDEX = Path('CASE_INDEX.md')

for p in (CASE, EVIDENCE, ROADMAP, INDEX):
    if not p.exists():
        raise SystemExit(f'missing required file: {p}')

# --- Case 76: add bounded cross-vendor manufacturer-contract deepening ---
case = CASE.read_text(encoding='utf-8')
case_heading = '### Solidigm 2025 + Micron 2026: cross-vendor product-contract corroboration, not a TLC/QLC physics experiment'
if case_heading not in case:
    marker = '\n---\n\n## Engineering reconstruction\n'
    if marker not in case:
        raise SystemExit('Case 76 engineering-reconstruction marker not found')
    section = r'''
### Solidigm 2025 + Micron 2026: cross-vendor product-contract corroboration, not a TLC/QLC physics experiment

The HPE pair above is useful because one OEM document places TLC and QLC products under a common retention clause, but it remains one document family and does not by itself answer the roadmap's cross-vendor corroboration gap. Two later manufacturer product briefs provide a bounded second check while also showing why equal-looking retention numbers must not be over-harmonized.

Solidigm's **D5-P5336** product brief, ©2025, identifies the drive family as **192-layer QLC NAND**. Its key-feature table states **`Power off Retention 3 months @ 40°C`** and separately publishes five-year endurance values ranging from **0.42 to 0.60 DWPD** across capacities from 7.68 TB to 122.88 TB, with corresponding PBW values. The endurance footnote further says the IU-aligned endurance figures use 100% random writes with 16 KB or 32 KB transfer geometry depending on SKU.[^solidigm-p5336]

Micron's **7600 NVMe SSD** product brief, Rev. B **07/2026**, identifies the family as using **Micron G9 TLC NAND**. It states **three months of data retention at 40 °C, power off at EOL**, and then separates two endurance classes: 7600 PRO is marketed as read-intensive at **1 DWPD**, while 7600 MAX is mixed-use at **3 DWPD**. Its specification table gives capacity-specific total-bytes-written values and notes that the endurance calculation assumes the drive is 100% full under 100% random aligned 4 KB writes; actual lifetime varies by workload.[^micron-7600]

The overlap is historically useful but narrow:

```text
Solidigm D5-P5336
    192L QLC NAND
    + 3 months @ 40°C power-off retention
    + one family of DWPD/PBW envelopes

Micron 7600
    G9 TLC NAND
    + 3 months @ 40°C power-off-at-EOL retention
    + different PRO/MAX DWPD/TBW envelopes
```

This establishes that by 2025–2026 **two different SSD manufacturers could publish the same numerical three-month / 40 °C power-off retention interval while using different media labels and different endurance/workload envelopes**. It strengthens the product-contract interpretation of the interval; it does not establish a media-only law.

Several controls are essential.

First, Solidigm's table does **not** use the same wording as Micron's: Solidigm gives `Power off Retention 3 months @ 40°C`, whereas Micron explicitly adds `power off at EOL`. The present evidence therefore does not silently upgrade the Solidigm sentence into an EOL clause or a JESD218 compliance statement.

Second, the endurance test descriptions are not matched. Solidigm's footnote uses IU-aligned 16 KB/32 KB random-write conditions for the quoted family endurance figures, whereas Micron's footnote describes 100% random aligned 4 KB writes at full user capacity for its TBW calculation. Therefore:

> **same numerical retention interval ≠ same endurance-stress workload**.

Third, the product families differ in capacity range, workload positioning, NAND generation, controller/firmware, correction margin, over-provisioning, interface generation, and other implementation details not controlled here. Therefore:

> **cross-vendor QLC/TLC product corroboration ≠ controlled QLC-versus-TLC experiment**.

And because these are vendor product briefs rather than independent qualification reports:

> **manufacturer contract corroboration ≠ independently audited standards compliance**.

The bounded result is consequently stronger than a single-OEM anecdote but weaker than a causal media comparison: the **service-level retention interval can recur across independently published TLC and QLC SSD product contracts while their host-write endurance envelopes and test wording remain distinct**.

'''
    case = case.replace(marker, '\n' + section + '---\n\n## Engineering reconstruction\n', 1)

status_insert = ('A 2025 Solidigm D5-P5336 QLC product brief and Micron 7600 Rev. B (07/2026) TLC product brief now add a bounded cross-vendor manufacturer-contract check: both publish a three-month / 40 °C power-off retention figure while their media labels, endurance envelopes, workload geometry, and exact wording differ. This corroborates recurrence of the service interval without turning it into a TLC/QLC cell-physics law or an independently audited compliance result.')
if status_insert not in case:
    gm = '\n\nGrounding record:'
    if gm not in case:
        raise SystemExit('Case 76 grounding-record marker not found')
    case = case.replace(gm, '\n\n' + status_insert + gm, 1)

case = case.replace(
    'A full pre-2000 EEPROM/Flash qualification genealogy, direct facsimile archaeology of original A117/A117B, the complete JESD219 workload history, later JESD218 revision history, and broader cross-vendor TLC/QLC qualification/fault evidence remain separate work best coordinated with `computing-archaeology`.',
    'A full pre-2000 EEPROM/Flash qualification genealogy, direct facsimile archaeology of original A117/A117B, the complete JESD219 workload history, later JESD218 revision history, controlled media-only TLC/QLC experiments, independent cross-vendor qualification/compliance evidence, and fault evidence remain separate work best coordinated with `computing-archaeology`.'
)

cross_result_anchor = ('The CM7 cross-check sharpens that warning: **same nominal capacity and the same family-level post-endurance retention interval ≠ a controlled TLC/QLC comparison**. The documented endurance ratings differ, but workload class, product generation, controller design, ECC margin, and other implementation variables are not held constant. The comparison therefore constrains product-contract interpretation without ranking the intrinsic retention physics of TLC and QLC.')
cross_result_add = cross_result_anchor + ('\n\nThe Solidigm/Micron cross-vendor check adds a different control: **same three-month / 40 °C power-off number across manufacturers ≠ same qualification wording, same endurance workload, same NAND physics, or same compliance path**. The recurrence is evidence about published SSD service contracts, not a controlled causal ranking of QLC and TLC media.')
if cross_result_anchor in case and 'The Solidigm/Micron cross-vendor check adds a different control' not in case:
    case = case.replace(cross_result_anchor, cross_result_add, 1)

if '[^solidigm-p5336]:' not in case:
    case = case.rstrip() + r'''

[^solidigm-p5336]: Solidigm, **_Solidigm D5-P5336 Product Brief_**, ©2025, especially the printed p. 3 `Solidigm D5-P5336 Key Feature Overview`: <https://www.solidigm.com/content/dam/solidigm/en/site/products/technology/p5336-product-brief/documents/Solidigm-D5P5336-ProductBrief.pdf>. The table identifies `192L QLC NAND`, `Power off Retention 3 months @ 40°C`, per-capacity five-year DWPD values, and PBW values. Footnote 17 states the IU-aligned endurance workload uses 100% random writes with 16 KB transfer units for 16 KB-IU SKUs and 32 KB for the 122.88 TB 32 KB-IU SKU.
[^micron-7600]: Micron Technology, **_Micron 7600 NVMe SSD Product Brief_**, Rev. B 07/2026, printed pp. 2–3: <https://my.micron.com/content/dam/micron/global/public/products/storage/ssds/data-center/7600/7600-nvme-ssd-product-brief.pdf>. Printed p. 2 identifies ninth-generation `TLC NAND` and states `3 months data retention @ 40 °C ... (power off at EOL)`; printed p. 3 identifies 7600 PRO as read-intensive / 1 DWPD and 7600 MAX as mixed-use / 3 DWPD, gives capacity-specific TBW figures, and notes that total-bytes-written calculations assume 100% random aligned 4 KB writes at full user capacity while actual lifetime varies by workload.
'''

CASE.write_text(case.rstrip() + '\n', encoding='utf-8')

# --- Evidence 76: add source ledger and explicit evidence limits ---
evidence = EVIDENCE.read_text(encoding='utf-8')
ev_heading = '## Source 11 — Solidigm D5-P5336 QLC + Micron 7600 TLC cross-vendor product-contract check, 2025–2026'
if ev_heading not in evidence:
    marker = '\n## Qualification-semantics deepening from the original JESD218 facsimile\n'
    if marker not in evidence:
        raise SystemExit('Evidence 76 qualification marker not found')
    ev_section = r'''
## Source 11 — Solidigm D5-P5336 QLC + Micron 7600 TLC cross-vendor product-contract check, 2025–2026

**Documents:**

- Solidigm, _Solidigm D5-P5336 Product Brief_, ©2025: <https://www.solidigm.com/content/dam/solidigm/en/site/products/technology/p5336-product-brief/documents/Solidigm-D5P5336-ProductBrief.pdf>;
- Micron Technology, _Micron 7600 NVMe SSD Product Brief_, Rev. B 07/2026: <https://my.micron.com/content/dam/micron/global/public/products/storage/ssds/data-center/7600/7600-nvme-ssd-product-brief.pdf>.

### Exact locations inspected

Solidigm D5-P5336, printed p. 3 / PDF page 3:

- `Media`: **192L QLC NAND**;
- `Power off Retention`: **3 months @ 40°C**;
- `Endurance (DWPD 5yrs)`: 0.42 / 0.53 / 0.56 / 0.58 / 0.60 across the listed capacities;
- `Endurance (PBW)`: 5.9 / 14.7 / 32.1 / 65.2 / 134.3;
- footnote 17: IU-aligned endurance based on **100% Random Write 16KB** for 16KB-IU SKUs and **100% Random Write 32KB** for the 122.88TB 32KB-IU SKU;
- final page: © Solidigm 2025.

Micron 7600, printed pp. 2–3:

- printed p. 2: the 7600 is identified as using **ninth-generation TLC NAND / G9 TLC NAND**;
- the same page states **3 months data retention @ 40 °C, power off at EOL**;
- printed p. 3: **7600 PRO — Read-Intensive, 1 Drive Write per Day**;
- printed p. 3: **7600 MAX — Mixed-Use, 3 Drive Writes per Day**;
- the same table publishes capacity-specific random/sequential TBW values and identifies the NAND again as **Micron G9 TLC NAND**;
- footnote 13: total bytes written are calculated at 100% full user capacity with **100% random aligned 4KB** writes; actual lifetime varies by workload;
- document footer: **Rev. B 07/2026**.

Both product tables were also checked on rendered PDF page images rather than relying only on text extraction/search snippets.

### What this source pair directly grounds

**Historical/product record:**

- by 2025 Solidigm publicly documented a named 192L QLC data-center SSD family with a three-month / 40 °C power-off retention specification and capacity-specific endurance figures;
- by July 2026 Micron publicly documented a named G9 TLC data-center SSD family with a three-month / 40 °C **power-off-at-EOL** retention statement and distinct 1-DWPD and 3-DWPD product classes;
- the same numerical retention interval therefore appears in independent manufacturer documentation over differently labeled NAND media and differently shaped host-write endurance envelopes.

**Engineering reconstruction:**

```text
same 3 months @ 40°C power-off number
    !=
same media label
    !=
same capacity range
    !=
same DWPD / PBW / TBW envelope
    !=
same endurance workload geometry
    !=
same exact retention wording
    !=
same controller / ECC / over-provisioning design
    !=
same standards-compliance path
```

This is the bounded cross-vendor corroboration that the earlier HPE-only TLC/QLC pair could not provide by itself.

### Evidence limit

These are **manufacturer product briefs**, not independent qualification-laboratory reports and not raw NAND-retention experiments. They do not expose threshold-voltage distributions, P/E-cycle distributions, ECC margin, wear-leveling state, internal refresh/rewrite policy, or qualification raw data.

The wording is also not identical. Micron explicitly says `power off at EOL`; the inspected Solidigm feature table says `Power off Retention 3 months @ 40°C` but does not, in that table, explicitly attach the interval to EOL or cite a JESD218 revision. The source pair therefore supports recurrence of a published **service-level number**, not a claim that both manufacturers used the same test method, the same JEDEC revision, or identical end-of-life semantics.

Finally, the quoted endurance workloads differ. A direct ratio between Solidigm DWPD/PBW and Micron TBW/DWPD cannot be attributed to `QLC` versus `TLC` because transfer geometry, product class, capacity, controller behavior, NAND generation, and other variables are not controlled.

---

'''
    evidence = evidence.replace(marker, '\n' + ev_section + '## Qualification-semantics deepening from the original JESD218 facsimile\n', 1)

EVIDENCE.write_text(evidence.rstrip() + '\n', encoding='utf-8')

# --- ROADMAP: close only the bounded cross-vendor manufacturer-contract gap ---
roadmap = ROADMAP.read_text(encoding='utf-8')
roadmap = roadmap.replace(
    'Direct normative JESD218A/JESD219A facsimiles, later B/C revision history, post-rating fault tests, broader cross-vendor TLC/QLC corroboration, and independent compliance testing remain open;',
    'Direct normative JESD218A/JESD219A facsimiles, later B/C revision history, post-rating fault tests, controlled media-only TLC/QLC comparison, and independent compliance testing remain open;'
)

new_bullet = ('- [x] Cross-vendor TLC/QLC manufacturer product-contract corroboration — canonical [`cases/76-jedec-ssd-endurance-retention-qualification.md`](cases/76-jedec-ssd-endurance-retention-qualification.md), with [`evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md`](evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md), now adds a 2025 Solidigm D5-P5336 manufacturer brief (192L QLC NAND; three months power-off retention at 40 °C; capacity-specific 0.42–0.60 DWPD/PBW envelope) and Micron 7600 Rev. B 07/2026 (G9 TLC NAND; three months at 40 °C power off at EOL; 7600 PRO 1 DWPD and MAX 3 DWPD). This closes only the bounded claim that the same numerical enterprise/data-center retention interval recurs in independent manufacturer product contracts across unlike media/workload/endurance envelopes. It does **not** close controlled TLC-vs-QLC media physics, identical qualification wording/test method, direct JESD218 revision compliance, independent laboratory verification, or post-rating fault testing.')
if new_bullet not in roadmap:
    lines = roadmap.splitlines()
    out = []
    inserted = False
    for line in lines:
        if line.startswith('- [x] Named QLC/TLC commercial-product post-endurance retention comparison —'):
            line = line.replace(
                'Cross-vendor TLC/QLC corroboration, direct later-JESD218 revision archaeology, independent compliance evidence, and post-rating fault tests remain open.',
                'The broader cross-vendor manufacturer-contract corroboration is now grounded in the separate bounded bullet below; controlled media-only TLC/QLC comparison, direct later-JESD218 revision archaeology, independent compliance evidence, and post-rating fault tests remain open.'
            )
            out.append(line)
            out.append(new_bullet)
            inserted = True
        else:
            out.append(line)
    if not inserted:
        raise SystemExit('ROADMAP named QLC/TLC bullet not found')
    roadmap = '\n'.join(out)
ROADMAP.write_text(roadmap.rstrip() + '\n', encoding='utf-8')

# --- CASE_INDEX: update Case 76 navigation row and append findings ---
index = INDEX.read_text(encoding='utf-8')
nav_note = 'cross-vendor manufacturer-contract corroboration now adds Solidigm D5-P5336 QLC and Micron 7600 TLC; controlled media-only comparison and independent compliance/fault evidence remain open'
if nav_note not in index:
    lines = index.splitlines()
    updated = False
    for i, line in enumerate(lines):
        if line.startswith('| [') and 'cases/76-jedec-ssd-endurance-retention-qualification.md' in line:
            if line.rstrip().endswith('|'):
                lines[i] = line.rstrip()[:-1].rstrip() + '; ' + nav_note + ' |'
            else:
                raise SystemExit('Case 76 index row does not end with table delimiter')
            updated = True
            break
    if not updated:
        raise SystemExit('Case 76 index navigation row not found')
    index = '\n'.join(lines)

findings_heading = '## Case 76 — Cross-vendor SSD retention-contract deepening findings'
if findings_heading not in index:
    findings = r'''

## Case 76 — Cross-vendor SSD retention-contract deepening findings

- **1713 — Solidigm D5-P5336 product record:** a 2025 Solidigm product brief directly places `192L QLC NAND`, `Power off Retention 3 months @ 40°C`, per-capacity five-year DWPD, and PBW in one named product-family table. (`H/P`)
- **1714 — Micron 7600 product record:** Micron 7600 Rev. B 07/2026 directly places `G9 TLC NAND`, `3 months ... @ 40 °C ... power off at EOL`, 7600 PRO `1 Drive Write per Day`, and 7600 MAX `3 Drive Writes per Day` in one named family contract. (`H/P`)
- **1715 — Same numerical interval ≠ same endurance envelope:** Solidigm and Micron publish the same three-month / 40 °C power-off number while exposing different DWPD/PBW/TBW envelopes. (`E`)
- **1716 — Same numerical interval ≠ same endurance workload:** Solidigm's quoted family endurance uses IU-aligned 16 KB/32 KB random-write conditions, while Micron's TBW calculation note uses 100% random aligned 4 KB writes at full user capacity. (`H/P`, `E`)
- **1717 — Same retention number ≠ identical wording:** Micron explicitly qualifies its statement as power off `at EOL`; the inspected Solidigm table does not add that phrase. The evidence therefore does not silently harmonize the two contracts. (`H/P`, `X`)
- **1718 — QLC/TLC label ≠ retention duration:** the recurrence of a three-month / 40 °C service figure across a QLC family and a TLC family blocks treating the published interval as a direct encoding of bits-per-cell alone. (`E`)
- **1719 — Product retention contract ≠ raw-cell retention law:** neither product brief exposes threshold-voltage distributions, cell-level retention curves, P/E dispersion, or raw error evolution sufficient for a media-physics conclusion. (`E`, `X`)
- **1720 — Cross-vendor corroboration ≠ controlled media experiment:** vendor, NAND generation, controller, ECC margin, over-provisioning, capacity range, interface generation, workload class, and endurance geometry differ. (`E`, `X`)
- **1721 — Manufacturer corroboration ≠ independent compliance:** two vendor briefs corroborate a published service-contract pattern but do not constitute an independent lab audit or direct evidence that the same JESD218 revision/test path was used. (`H/P`, `X`)
- **1722 — DWPD/PBW/TBW difference ≠ causal TLC/QLC ranking:** the product documents do not hold the other causal variables constant, so endurance ratios cannot be attributed to media density label alone. (`E`, `X`)
- **1723 — Same service interval can sit above unlike prior histories:** a common power-off retention duration can be specified above different host-write workloads and endurance boundaries; the retention clock therefore remains conditioned by a larger product qualification relation. (`E`)
- **1724 — HPE pair and cross-vendor pair answer different questions:** the HPE CM7/P5430 comparison holds OEM document family and nominal capacity constant while other variables differ; the Solidigm/Micron comparison adds manufacturer independence but relaxes capacity/workload comparability. Neither is a controlled NAND experiment. (`E`)
- **1725 — Related-repository boundary:** searches of `tmzncty/computing-archaeology` for `D5-P5336` and `Micron 7600` returned no dedicated case to reuse. This deepening therefore stays retention-specific here; broad NAND/SSD product genealogy remains companion-repository work. (`H/P` project-state record)
'''
    index = index.rstrip() + findings

INDEX.write_text(index.rstrip() + '\n', encoding='utf-8')

# --- Local validation before workflow commit ---
checks = {
    CASE: [case_heading, '[^solidigm-p5336]:', '[^micron-7600]:', 'manufacturer contract corroboration ≠ independently audited standards compliance'],
    EVIDENCE: [ev_heading, 'Power off Retention 3 months @ 40°C', 'power off at EOL', 'same 3 months @ 40°C power-off number'],
    ROADMAP: ['Cross-vendor TLC/QLC manufacturer product-contract corroboration', 'controlled media-only TLC/QLC comparison'],
    INDEX: [findings_heading, '**1713 — Solidigm D5-P5336 product record:**', '**1725 — Related-repository boundary:**', nav_note],
}
for path, needles in checks.items():
    text = path.read_text(encoding='utf-8')
    for needle in needles:
        if needle not in text:
            raise SystemExit(f'validation failed: {needle!r} missing from {path}')
