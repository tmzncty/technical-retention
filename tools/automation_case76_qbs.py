from pathlib import Path
import re

ROOT = Path('.')

EVIDENCE = ROOT / 'evidence/76-lattice-2014-qualified-by-similarity-retention-deepening.md'
CASE = ROOT / 'cases/76-jedec-ssd-endurance-retention-qualification.md'
ROADMAP = ROOT / 'ROADMAP.md'
INDEX = ROOT / 'CASE_INDEX.md'


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected one anchor, found {count}: {old[:100]!r}')
    path.write_text(text.replace(old, new, 1), encoding='utf-8')


if EVIDENCE.exists():
    raise SystemExit(f'{EVIDENCE} already exists; refusing duplicate research slice')

EVIDENCE.write_text(r'''# Case 76 Deepening — Lattice 2014 Qualified-by-Similarity Retention Qualification Coverage

## Status

**`grounded follow-up`** — bounded to one manufacturer-primary example of how nonvolatile-memory endurance/data-retention qualification evidence can be generated on a source qualification vehicle and extended to another product family through an explicit documented similarity relation.

This record does **not** claim that Lattice invented qualification by similarity, that every LA-MachXO device was directly subjected to the same high-temperature retention stress, that a zero-failure qualification sample implies zero field failures, or that device-level Flash qualification is equivalent to JESD218 SSD-level endurance qualification.

## Research question

> When a product family cites nonvolatile-memory cycling/endurance and high-temperature data-retention qualification, what was directly stressed, what was covered by a similarity relation, and what does that coverage not prove?

The retention-specific point is that a qualification statement may depend on more than a stress recipe and a pass/fail result. It can also depend on a retained **qualification relation** connecting a tested vehicle to a covered target family.

---

## Sources

### 1. Lattice Semiconductor, *LA-MachXO Product Family AEC-Q100 Qualification Summary*, December 2014

- Document: Lattice Semiconductor Corporation Doc. **25-107420 Rev. A**, December 2014.
- Manufacturer copy / current document route: <https://www.latticesemi.com/view_document?document_id=50838>
- Alternate manufacturer asset path surfaced by Lattice search indexing: <https://www.latticesemi.com/-/media/LatticeSemi/Documents/ProductChangeNotification/PCN14/PCN07A14LAXOqualsum107420.ashx?document_id=50838>

Relevant locations in the indexed document text:

- §2 identifies AEC-Q100 Rev. H as the qualification framework and states that the qualification had no listed deviations from it.
- Test Group B identifies `NVCE + HTDR (Non-volatile Cycling Endurance + High Temp Data Retention)` as test B3 and names **LAXP2-17E-FTN256** as the qualification vehicle.
- The note directly below B3 says LA-MachXO uses the **same Flash memory cells** and is fabricated in the **same wafer fab** as LAXP2; it explicitly says LA-MachXO Flash NVCE + HTDR is **Qualified-by-Similarity** from LAXP2 data under the AEC-Q100 product-qualification-family concept.
- The detailed retention text says all cells in all arrays are tested in programmed and erased states and that LAXP2 devices are program/erase cycled **10,000 times** before data-retention stress.
- The detailed result table lists LAXP2-17E lots 8, 9, and 10 with quantities **100, 80, and 80**, each reporting zero failures.
- A separate `Extended NVCE` line uses 80 LAMXO2280E units in a room/hot and check/check# split and reports zero failures through **40,000 P/E cycles**.

### 2. Lattice Semiconductor, *LatticeXP2 Product Family Qualification Summary*

- Manufacturer asset: <https://www.latticesemi.com/~/media/98C2B381B2B14DE3B7936031B28ABA33.ashx>

Relevant indexed text:

- §3.2 describes High Temperature Data Retention (`HTRX`) as a test intended to accelerate charge gain/loss on floating gates and to measure reliability of programmed information retention.
- It states that all cells in all arrays are life-tested in both programmed and erased states and that products are preconditioned to maximum datasheet program/erase-cycle conditions.
- LFXP2/LAXP2 HTRX conditions are **168, 500, and 1000 hours at 150 °C**, using Lattice method 87-101925 and **JESD22-A103C / JESD22-A117A**.
- Table 3.2.1 lists LAXP2-17E lots 8/9/10 at 100/80/80 units with zero failures through the listed intervals, plus 102 LFXP2-40E units with zero failures; the table reports a cumulative HTRX result of **0 / 362** and **362,000 device-hours**.

These are manufacturer-primary qualification records. They establish Lattice's own qualification procedure, evidence, and coverage rationale; they are not independent field-failure audits.

---

## Historical record

### A tested qualification vehicle and a covered product family are not the same object

The December 2014 LA-MachXO summary does not present B3 as though every LA-MachXO density/package combination had independently undergone the identical retention sequence. It names **LAXP2-17E-FTN256** as the B3 vehicle and then supplies a reason for transferring the result: LA-MachXO uses the same Flash cells and the same wafer fab as LAXP2, which Lattice treats as satisfying the cited product-family similarity relation.

That is a historically explicit manufacturer distinction:

```text
directly stressed qualification vehicle
        !=
product family covered by qualification
```

The term `Qualified-by-Similarity` is Lattice's own 2014 vocabulary here. It is not a project label projected backward.

### The source qualification data combine cycling preconditioning with accelerated retention stress

The LA-MachXO record says the source LAXP2 devices were cycled 10,000 times before retention testing, with Flash cells exercised in both programmed and erased states. The LatticeXP2 family summary independently specifies 150 °C HTRX intervals of 168, 500, and 1000 hours and reports zero failures for the three named LAXP2-17E lots in its table.

The bounded historical relation is therefore:

```text
P/E preconditioning
    -> accelerated high-temperature retention stress
    -> observed qualification result on named source lots
```

It is not a direct observation of the target field lifetime at normal use temperature.

### Lattice also ran target-family cycling work without silently equating it to the source HTRX dataset

The same LA-MachXO qualification summary separately reports an 80-unit `Extended NVCE` split on LAMXO2280E with no failures through 40,000 P/E cycles. That target-family exercise strengthens the manufacturer qualification package, but it is listed separately from the source-family B3 retention vehicle and therefore should not be rewritten as though all LA-MachXO devices directly repeated the full LAXP2 HTRX matrix.

This matters because `some direct target-family stress` and `the stress dataset carrying the qualification-by-similarity claim` are different evidence roles.

---

## Engineering reconstruction

### Qualification coverage is a relation, not merely a test result

For this bounded example, the evidence chain is better represented as:

```text
stress method
    + source qualification vehicle
    + observed source result
    + documented similarity criteria
    -> qualification coverage claim for target family
```

The fourth term is not payload data and is not a physical retention mechanism. It is **qualification-control evidence**: the documented relation that authorizes reuse of prior test results for another product family.

Therefore:

> **standardized stress method != qualification coverage rule**

and:

> **directly stressed device != every device covered by the qualification statement**.

### Similarity is scope-qualified

Lattice's stated transfer rationale is specific: same Flash memory cells and same wafer fab, under the product-family rule it cites. Even if that relation is accepted for the NVM endurance/retention claim, it does not prove identity of every package, high-voltage circuit, board environment, assembly mechanism, or whole-device failure envelope.

Thus:

> **same Flash cell / wafer-fab basis != identical whole-device reliability envelope**.

A package or process change can also matter to requalification policy even when the retained NVM mechanism is unchanged. The exact AEC-Q100 requalification rules are outside this slice because the normative Appendix 1 text was not directly inspected here.

### Qualification samples do not become deterministic lifetime guarantees

The reported zero failures are observations over bounded samples and stress conditions. They do not support:

```text
0 observed failures in qualification sample
    -> 0 probability of field failure
```

Nor does 1000 hours at 150 °C become a literal statement that every field device was observed for a corresponding number of years. Case 132 already handles the separate accelerated-retention / stress-to-use transformation boundary; this case only records that the qualification evidence here is accelerated and sample-bounded.

### Device-level NVM qualification is not the JESD218 SSD service contract

JESD22-A117 appears here inside a semiconductor-device Flash endurance/data-retention test regime. Case 76's main JESD218 evidence concerns a later and different SSD-level relation involving host-written TBW, workload, capacity, UBER/FFR, and subsequent power-off retention.

The shared words `endurance` and `data retention` do not erase the level difference:

```text
Flash-array/device qualification
    !=
SSD host-interface service-envelope qualification
```

This manufacturer example therefore deepens the earlier A117→JESD218 prior-art boundary without implying direct genealogy from this Lattice product family to SSD standards.

---

## Functional comparisons — explicitly non-genealogical

- **Case 132:** accelerated retention stress and later use-condition interpretation are functionally related evidence layers, but Case 132 owns the temperature/Arrhenius transformation problem; this record does not reproduce that history.
- **Case 38:** manufacturer validation, component-local self-test, and independent system fault observation are distinct assurance layers. The comparison is only that `evidence role` must be typed; it does not assert common qualification machinery between SSD power-loss protection and FPGA Flash retention.

---

## Rejected upgrades / stop conditions

This slice does **not** establish any of the following:

1. Lattice invented qualification by similarity or product-family qualification.
2. JESD22-A117 originated with Lattice, AEC-Q100, or the 2014 documents.
3. Every LA-MachXO SKU/package/lot was directly subjected to the same 150 °C HTRX sequence.
4. Zero failures in the cited qualification sample imply zero field-failure probability.
5. 1000 hours at 150 °C directly equals a field-retention lifetime without a specified stress-to-use model.
6. The QBS rationale proves identical package, power, configuration-control, or whole-device failure behavior.
7. The 40,000-cycle LA-MachXO extension is the same evidence object as the LAXP2 HTRX dataset.
8. Device-level Flash NVCE/HTDR is equivalent to JESD218 SSD TBW qualification.
9. The 2014 document proves invention priority or first industry use of `Qualified-by-Similarity`.
10. A manufacturer qualification summary is an independent compliance audit or field reliability study.

---

## Related-repository check

`tmzncty/computing-archaeology` was searched for `JESD22-A117`, `Qualified-by-Similarity`, `Lattice MachXO`, and the combined qualification topic before writing this slice. No dedicated semiconductor-qualification history was found in the current indexed repository.

The division of labor remains:

- this repository keeps the **retention-specific evidence relation** — direct stress, accelerated retention, similarity-qualified coverage, and the limits of the resulting claim;
- `computing-archaeology` should own a broader history of semiconductor product-family qualification, AEC/JEDEC generic-data rules, process-transfer qualification, and vendor genealogy if that history is later built.

---

## Remaining work

A later slice may deepen one of these without reopening the bounded result above:

- directly inspect the normative AEC-Q100 Rev. H Appendix 1 product-family / generic-data language cited by Lattice;
- directly inspect original JESD22-A117A/C facsimiles rather than relying on the manufacturer's standards references plus the existing later JEDEC revision ledger;
- add another vendor's named qualification-by-similarity or generic-data retention example;
- recover exact requalification triggers when Flash cell, wafer fab, process, package, or assembly site changes;
- add independent fault/retention validation for a named product;
- route broad semiconductor-qualification genealogy to `computing-archaeology`.

The closed result for Case 76 is narrower:

> **A retention/endurance qualification claim can validly cover a target family through an explicitly documented similarity relation even when the decisive retention stress was run on a source qualification vehicle; therefore qualification coverage must not be silently read as per-SKU direct stress, and a bounded passing sample must not be promoted into a deterministic lifetime guarantee.**
''', encoding='utf-8')

# Case 76 navigation + concise canonical synthesis.
case_text = CASE.read_text(encoding='utf-8')
link_line = ('Qualification-coverage deepening: '
             '[`../evidence/76-lattice-2014-qualified-by-similarity-retention-deepening.md`]'
             '(../evidence/76-lattice-2014-qualified-by-similarity-retention-deepening.md).')
if link_line not in case_text:
    anchor = ('Grounding record: [`../evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md`]'
              '(../evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md).')
    if case_text.count(anchor) != 1:
        raise SystemExit('Case 76 grounding-record anchor missing or duplicated')
    case_text = case_text.replace(anchor, anchor + '\n\n' + link_line, 1)

subheading = '### Manufacturer qualification coverage can extend beyond directly stressed samples'
if subheading not in case_text:
    anchor2 = '### JESD218 makes endurance and retention separate concepts, then composes them'
    if case_text.count(anchor2) != 1:
        raise SystemExit('Case 76 historical subsection anchor missing or duplicated')
    insert = r'''### Manufacturer qualification coverage can extend beyond directly stressed samples

A December-2014 Lattice LA-MachXO AEC-Q100 qualification summary adds a useful evidence-layer boundary below the SSD-level JESD218 contract. For `NVCE + HTDR`, Lattice names LAXP2-17E as the qualification vehicle and explicitly says LA-MachXO Flash endurance/data retention is **Qualified-by-Similarity** because the families use the same Flash cells and the same wafer fab under the cited product-family rule. The accompanying data say the source LAXP2 devices were P/E-cycled 10,000 times before retention stress, with cells exercised in programmed and erased states; a LatticeXP2 family summary gives 150 °C HTRX intervals through 1000 hours and zero failures for the named LAXP2 lots. A separate 80-unit LA-MachXO extended-cycling exercise reports zero failures through 40,000 cycles.

The historical vocabulary therefore supports a distinction that should not be erased in later summaries:

```text
directly stressed qualification vehicle
    !=
target family covered by a documented similarity relation
```

**Engineering reconstruction:** qualification coverage depends on a chain of stress method + source vehicle + observed result + similarity criteria. `Standard test method != qualification coverage rule`; `covered family != every covered SKU directly stressed`; `same Flash cell / wafer fab != identical whole-device failure envelope`; and `0 observed failures in a bounded qualification sample != zero field-failure probability`. The high-temperature stress is also accelerated evidence, not literal observation of the target field lifetime; Case 132 owns that separate stress-to-use boundary.

This does not collapse device-level Flash qualification into JESD218. The Lattice evidence is a semiconductor NVM endurance/retention qualification relation, whereas JESD218 composes host-written TBW, workload, SSD-level error/failure criteria, and subsequent power-off retention. The shared vocabulary is historical overlap, not proof of identical qualification objects or genealogy.

'''
    case_text = case_text.replace(anchor2, insert + anchor2, 1)
CASE.write_text(case_text, encoding='utf-8')

# Roadmap completion bullet placed immediately after the existing A117 -> JESD218 bullet.
road = ROADMAP.read_text(encoding='utf-8')
road_title = '- [x] JESD22-A117 → JESD218 qualification-layer prior-art deepening'
new_bullet = ('- [x] **Case 76 Lattice qualification-by-similarity coverage deepening** — '
              '[`cases/76-jedec-ssd-endurance-retention-qualification.md`](cases/76-jedec-ssd-endurance-retention-qualification.md) + '
              '[`evidence/76-lattice-2014-qualified-by-similarity-retention-deepening.md`](evidence/76-lattice-2014-qualified-by-similarity-retention-deepening.md): '
              'Lattice\'s December-2014 LA-MachXO AEC-Q100 summary explicitly extends Flash NVCE/HTDR qualification from an LAXP2 source vehicle to LA-MachXO by `Qualified-by-Similarity` on the stated same-cell/same-wafer-fab basis, while separate source-family HTRX and target-family extended-cycling data keep direct stress distinct from covered qualification. This closes the bounded `standard stress method != coverage rule`, `directly stressed vehicle != every covered SKU`, `sample pass != deterministic field lifetime`, and `device-level NVM qualification != JESD218 SSD service contract` seams. Direct AEC-Q100 Appendix-1 / original A117A/C facsimiles, cross-vendor generic-data practice, process-change requalification, and independent named-product retention testing remain open; broad qualification genealogy belongs in `computing-archaeology`.')
if new_bullet not in road:
    start = road.find(road_title)
    if start < 0:
        raise SystemExit('ROADMAP A117 bullet anchor not found')
    end = road.find('\n\n', start)
    if end < 0:
        raise SystemExit('ROADMAP A117 bullet paragraph terminator not found')
    road = road[:end] + '\n\n' + new_bullet + road[end:]
ROADMAP.write_text(road, encoding='utf-8')

# Append canonical findings using the current maximum numeric finding id.
index = INDEX.read_text(encoding='utf-8').rstrip() + '\n'
section_heading = '## Case 76 — Lattice qualification-by-similarity retention-coverage deepening findings'
if section_heading not in index:
    ids = [int(x) for x in re.findall(r'- \*\*(\d+) —', index)]
    if not ids:
        raise SystemExit('No numeric findings found in CASE_INDEX')
    n = max(ids) + 1
    findings = [
        ('December-2014 LA-MachXO qualification explicitly uses a source qualification vehicle', 'Lattice Test Group B names LAXP2-17E-FTN256 for NVCE + HTDR rather than representing every LA-MachXO combination as independently stressed.', 'H/P'),
        ('Lattice explicitly uses Qualified-by-Similarity vocabulary', 'the LA-MachXO summary says the target-family Flash NVCE + HTDR is Qualified-by-Similarity from LAXP2 data under the cited product-qualification-family rule.', 'H/P'),
        ('the stated transfer basis is same Flash cells plus same wafer fab', 'this is the manufacturer-recorded rationale for the bounded NVM qualification transfer; it is not a project-invented similarity criterion.', 'H/P'),
        ('source retention testing covers programmed and erased Flash states', 'Lattice says all cells in all arrays are life-tested in both programmed and erased states for the cited retention qualification.', 'H/P'),
        ('LAXP2 source devices are preconditioned by 10,000 P/E cycles', 'the LA-MachXO qualification record states that LAXP2 devices are programmed and erased 10,000 times before data-retention testing.', 'H/P'),
        ('the LatticeXP2 HTRX record uses accelerated 150 °C stress through 1000 hours', 'the manufacturer family summary specifies 168/500/1000-hour HTRX intervals at 150 °C and cites JESD22-A103C/A117A.', 'H/P'),
        ('named LAXP2 HTRX lots report zero failures in the published table', 'lots 8/9/10 are listed at 100/80/80 units with zero failures; an additional LFXP2 lot yields a published cumulative 0/362 and 362,000 device-hours.', 'H/P'),
        ('LA-MachXO also has separate target-family extended-cycling evidence', 'the automotive summary reports an 80-unit LAMXO2280E split with zero failures through 40,000 P/E cycles, separately from the source-family HTRX evidence.', 'H/P'),
        ('standard stress method is not the qualification coverage rule', 'a JESD/AEC-referenced test procedure defines stress/measurement, while the source-to-target similarity relation defines why prior results are allowed to cover another family.', 'E'),
        ('directly stressed vehicle is not every device covered by qualification', 'qualification coverage can be relational: tested vehicle + result + accepted similarity criteria can support a broader product-family claim.', 'E'),
        ('same Flash cell and wafer fab do not prove whole-device equivalence', 'the bounded QBS rationale is not upgraded into identity of packages, high-voltage circuits, assembly behavior, or every system-level failure mode.', 'X'),
        ('zero observed qualification failures do not imply zero field-failure probability', 'bounded samples and stress durations cannot be promoted into a deterministic per-device lifetime guarantee.', 'X'),
        ('accelerated retention duration is not literal field lifetime', 'the 150 °C HTRX interval is qualification evidence; stress-to-use transformation requires a separate model, handled comparatively in Case 132.', 'E/A'),
        ('device-level Flash retention qualification is not the JESD218 SSD service contract', 'the former qualifies NVM cells/devices under cycling/retention stress, while the latter composes host TBW, workload, SSD error/failure criteria, and later power-off retention.', 'E/A'),
        ('qualification coverage depends on retained relation evidence as well as retained test results', 'for a QBS claim to remain interpretable, later users need both the source result and the documented basis authorizing transfer to the target family.', 'E'),
        ('the 2014 Lattice record is a documentation floor, not an invention-priority claim', 'it proves this named manufacturer used QBS vocabulary and practice by December 2014 but not first industry use, origin of AEC generic-data policy, or origin of JESD22-A117.', 'X'),
    ]
    lines = ['\n' + section_heading, '', 'Deepening record: [`evidence/76-lattice-2014-qualified-by-similarity-retention-deepening.md`](evidence/76-lattice-2014-qualified-by-similarity-retention-deepening.md).', '']
    for title, body, label in findings:
        lines.append(f'- **{n} — {title}:** {body} (`{label}`)')
        n += 1
    index += '\n'.join(lines) + '\n'
INDEX.write_text(index, encoding='utf-8')

# Basic integration guards.
for p in [EVIDENCE, CASE, ROADMAP, INDEX]:
    text = p.read_text(encoding='utf-8')
    if '\r\n' in text:
        raise SystemExit(f'{p}: CRLF introduced unexpectedly')

if '76-lattice-2014-qualified-by-similarity-retention-deepening.md' not in CASE.read_text(encoding='utf-8'):
    raise SystemExit('Case navigation missing new evidence')
if 'Case 76 Lattice qualification-by-similarity coverage deepening' not in ROADMAP.read_text(encoding='utf-8'):
    raise SystemExit('Roadmap completion bullet missing')
if section_heading not in INDEX.read_text(encoding='utf-8'):
    raise SystemExit('CASE_INDEX findings section missing')

print('Case 76 QBS retention-qualification deepening integrated successfully')
