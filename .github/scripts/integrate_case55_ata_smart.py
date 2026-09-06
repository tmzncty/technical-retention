from pathlib import Path

CASE_PATH = Path('cases/55-nvme-smart-health-endurance-telemetry.md')
EVIDENCE_PATH = Path('evidence/55-nvme10-13-smart-health-endurance-grounding.md')
ROADMAP_PATH = Path('ROADMAP.md')
INDEX_PATH = Path('CASE_INDEX.md')


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: expected exactly one anchor, found {count}')
    return text.replace(old, new, 1)


def insert_before_once(text: str, anchor: str, addition: str, label: str) -> str:
    count = text.count(anchor)
    if count != 1:
        raise RuntimeError(f'{label}: expected exactly one anchor, found {count}')
    return text.replace(anchor, addition + anchor, 1)


case = CASE_PATH.read_text(encoding='utf-8')
evidence = EVIDENCE_PATH.read_text(encoding='utf-8')
roadmap = ROADMAP_PATH.read_text(encoding='utf-8')
index = INDEX_PATH.read_text(encoding='utf-8')

# ---------------------------------------------------------------------------
# Case 55: add a bounded ATA SMART prior-art floor without turning the case
# into a full SMART genealogy.
# ---------------------------------------------------------------------------
case = replace_once(
    case,
    'The latest deepening uses the original 2011 Gold specification to separate spare-threshold warning, reserve exhaustion, and actual command failure without inferring a hidden SSD remapping algorithm.',
    'The spare-exhaustion deepening uses the original 2011 Gold specification to separate spare-threshold warning, reserve exhaustion, and actual command failure without inferring a hidden SSD remapping algorithm. A new prior-art pass adds a bounded 1995–1997 ATA SMART floor for retained drive-health state, while explicitly refusing to equate ATA vendor-specific attributes with the later NVMe SMART / Health schema or to claim a direct ATA→NVMe genealogy.',
    'case status deepening',
)

historical_add = r'''### 1995–1997 ATA SMART supplies an older drive-health-state floor without supplying the NVMe schema

The NVMe interface is not the beginning of drive-health state retention. An official **July 1995 X3T10 SFF Liaison Report (`95-292r0`)** states that a copy of `SMART (Self Monitoring Analysis and Reporting Technology)` submitted by Quantum had been approved for publication as **SFF-8035i**. The document is useful as a standards-history floor, but it does **not** prove that Quantum invented SMART or that the inspected copy contains every semantic detail later carried into ATA.

The later **ATA-3 Working Draft X3T13/2008D Revision 7b, 27 January 1997** provides the needed interface semantics. Its revision history records that Revision 3, dated **26 July 1995**, `Added SFF8035i S.M.A.R.T. into the standard`. Clause 6.6 then describes SMART as monitoring and **storing** performance/calibration parameters to predict near-term degradation or fault conditions. The draft is explicit that the set and identity of attributes are selected by the device manufacturer and are vendor-specific/proprietary, while thresholds are manufacturer-determined from design/reliability testing.

That distinction matters for this case. ATA-3 does not present one fixed cross-vendor health schema equivalent to the later NVMe log. It presents a host interface around a manufacturer-selected attribute/threshold model.

The same draft also gives direct retention semantics for the monitoring machinery itself:

- `SMART DISABLE OPERATIONS` says the enabled/disabled SMART state is preserved across power cycles;
- `SMART ENABLE/DISABLE ATTRIBUTE AUTOSAVE` allows updated attribute values to be saved to **nonvolatile memory** after vendor-specified events, and preserves the autosave enabled/disabled state across power cycles;
- `SMART READ ATTRIBUTE VALUES` saves updated values to nonvolatile memory before returning the attribute-value structure;
- `SMART RETURN STATUS` saves updated values to nonvolatile memory before comparing them with the thresholds;
- `SMART SAVE ATTRIBUTE VALUES` explicitly forces updated values into nonvolatile memory regardless of the autosave timer.

The bounded historical result is therefore stronger than the generic statement `SMART existed before NVMe`:

```text
manufacturer-selected monitored attribute
        -> retained/updated attribute value
        -> manufacturer-set threshold
        -> threshold comparison / reliability status
        -> host-visible warning relation
```

with a separate policy/control path:

```text
SMART enabled state
attribute-autosave enabled state
        -> preserved across power cycles
```

and a separate materialization step:

```text
updated attribute value
        -> optional/event- or command-triggered save to nonvolatile memory
```

These arrows are an **engineering reconstruction of the documented interface relations**, not period terminology and not a claim that every ATA device implemented the same internal sensors, media, firmware, or persistence mechanism.

The source boundary is also explicit. The ATA-3 text inspected here is a period **working draft** preserved through a third-party transcription/mirror. Its document identity, revision/date, clause structure, and wording are strong enough for this bounded standards-history comparison, but the project does not silently upgrade the mirror into a directly inspected original SFF-8035i facsimile or use it to settle SMART invention priority.

'''
case = insert_before_once(
    case,
    '### NVMe 1.0 already separates spare threshold, spare exhaustion, and command failure\n',
    historical_add,
    'case historical insertion',
)

engineering_add = r'''### Same `SMART` label does not imply the same retained schema

ATA-3 and NVMe both expose device-health state to a host, but the inspected contracts are not interchangeable. ATA-3 says the active attribute set and attribute identities are manufacturer-selected and proprietary; NVMe instead standardizes named fields such as `Available Spare`, `Percentage Used`, `Data Units Written`, power-cycle counts, and media/data-integrity error counts.

Therefore:

> **ATA SMART attribute state ≠ NVMe SMART / Health field schema**.

and:

> **shared `SMART` terminology ≠ unchanged semantics or proven implementation genealogy**.

The earlier ATA source is prior art for **retained drive-health state and host-visible reliability qualification**, not evidence that NVMe copied a particular ATA attribute representation or that the two interfaces share one internal health model.

### Monitoring policy state, observed health state, and nonvolatile save are separate relations

ATA-3 preserves SMART enable/disable state and autosave policy across power cycles, while separately describing when updated attribute values are monitored and when they are saved to nonvolatile memory. An enabled autosave policy is therefore not itself a stored attribute value, and enabling SMART is not equivalent to saying that every possible health observation has already been materialized persistently.

Therefore:

> **SMART enabled state ≠ attribute value**,

> **attribute-autosave policy ≠ autosave event ≠ nonvolatile attribute embodiment**.

The command descriptions add a useful counterexample to a passive-observation model: `READ ATTRIBUTE VALUES` and `RETURN STATUS` can cause updated health values to be saved before the host receives data/status. In this bounded ATA contract, observation/reporting can be coupled to **maintenance of the telemetry state itself**.

This still does not mean the attribute records are a complete event history. They compress device-specific conditions into normalized values/status, just as later NVMe counters/estimates compress other aspects of use and degradation.

'''
case = insert_before_once(
    case,
    '### The device can retain evidence about its own retention margin\n',
    engineering_add,
    'case engineering insertion',
)

case = replace_once(
    case,
    'This case does not attempt a full ATA SMART genealogy or claim that NVMe invented drive-health monitoring. That history belongs in a separate bounded standards/genealogy slice if needed.',
    '''The prior-art boundary is now narrower. Official July 1995 T10/SFF evidence establishes publication approval for SFF-8035i, and the January 1997 ATA-3 Revision 7b working draft records the July 1995 incorporation of SFF8035i SMART and directly grounds manufacturer-selected attributes, thresholds, nonvolatile attribute saves, and power-cycle-persistent SMART/autosave policy state. This is enough to reject any NVMe-origin reading of drive-health retention.\n\nIt is **not** a full ATA SMART genealogy. The original SFF-8035i facsimile/revision chain, pre-SFF vendor implementations, ATA-4/ATA-5 changes, offline data collection/self-test evolution, named-product attribute meanings, and any direct ATA→NVMe design genealogy remain separate work. `SFF publication approval`, `ATA-3 incorporation`, and `invention` are not treated as synonyms.''',
    'case prior-art replacement',
)

case_claim_rows = r'''| July 1995 X3T10/SFF liaison evidence says a Quantum-submitted SMART copy was approved for publication as SFF-8035i | `H/P` | strong official committee liaison witness; publication floor, not invention proof |
| ATA-3 Revision 7b records that its 26 July 1995 Revision 3 added SFF8035i SMART | `H/P` | strong period working-draft revision history, mirror provenance retained |
| ATA-3 SMART attributes/identities are manufacturer-selected and proprietary, while thresholds are manufacturer-set | `H/P` | strong period working-draft semantics |
| ATA-3 preserves SMART enable state and attribute-autosave policy across power cycles and can save updated attribute values to nonvolatile memory | `H/P` | strong period working-draft command semantics |
| ATA SMART attribute state is historically/technically identical to the later fixed NVMe SMART / Health field schema | `X` | rejected; shared label does not erase interface/schema differences |
| SFF-8035i publication approval or ATA-3 incorporation proves invention priority or direct ATA→NVMe genealogy | `X` | rejected; standards-history floor only |
'''
case = replace_once(
    case,
    '| --- | --- | --- |\n',
    '| --- | --- | --- |\n' + case_claim_rows,
    'case claim-ledger rows',
)

source_add = r'''7. X3T10, **Liaison Report from SFF**, `X3T10/95-292r0`, July 1995; official T10 archive, directly inspected facsimile p. 1: <https://www.t10.org/ftp/t10/document.95/95-292r0.pdf>
8. X3T13, **AT Attachment-3 Interface (ATA-3), Working Draft X3T13/2008D Revision 7b**, 27 January 1997; period draft text/transcription used for §6.6 and §7.31 semantics and revision history: <https://paperzz.com/doc/7545036/at-attachment-3-interface--ata-3--working-draft>
'''
case = replace_once(
    case,
    '\n## Related repositories\n',
    '\n' + source_add + '\n## Related repositories\n',
    'case sources insertion',
)

case = replace_once(
    case,
    'A repository search found no dedicated NVMe SMART/endurance case in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology). Broader SSD/NAND engineering chronology should remain there if developed; this case keeps only the retention-specific interface/history distinction.',
    'A fresh repository search found no dedicated NVMe SMART/endurance or ATA SMART/SFF-8035i case in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology). Broader SMART/ATA/NVMe health-monitoring genealogy and disk/SSD engineering chronology should remain there if developed; this case keeps only the retention-specific state/history and interface-boundary distinctions.',
    'case related-repo update',
)

# ---------------------------------------------------------------------------
# Evidence 55: preserve source provenance and exact bounded claims.
# ---------------------------------------------------------------------------
evidence = replace_once(
    evidence,
    'The answer is yes for the bounded NVMe 1.0–1.3 record. The original 2011 Gold revision additionally grounds the boundary between spare-threshold warning, lack of spare locations, and command failure.',
    'The answer is yes for the bounded NVMe 1.0–1.3 record. The original 2011 Gold revision additionally grounds the boundary between spare-threshold warning, lack of spare locations, and command failure. A new bounded prior-art pass adds an official July 1995 T10/SFF publication witness and a January 1997 ATA-3 working-draft semantics witness, establishing that retained drive-health state, threshold qualification, nonvolatile attribute saving, and power-cycle-persistent monitoring policy predate NVMe without claiming a complete SMART genealogy.',
    'evidence opening update',
)

prior_sources = r'''## Source F — X3T10 SFF liaison report, July 1995

**Document:** Dal Allan, `Liaison Report from SFF`, **X3T10/95-292r0**.  
**Archive/date anchor:** official T10 1995 document index labels the item `Liaison Report from SFF - 7/95`.  
Official PDF: <https://www.t10.org/ftp/t10/document.95/95-292r0.pdf>

The two-page official facsimile was directly inspected. On printed p. 1 the report states that a copy of SMART — expanded there as `Self Monitoring Analysis and Reporting Technology` — submitted by Quantum had been **approved for publication as SFF-8035i**.

### Directly supported

- By July 1995, SFF committee work had an identifiable `SMART` document approved for publication as `SFF-8035i`.
- The liaison report associates the submitted copy with Quantum.
- `SMART` was already expanded as `Self Monitoring Analysis and Reporting Technology` in this committee record.

### Does not support

- Quantum invention priority;
- first proprietary implementation date;
- exact contents/revision of the approved SFF-8035i text;
- direct genealogy into every later ATA or NVMe SMART mechanism.

The source is used as a **publication/standardization floor**, not an invention certificate.

## Source G — ATA-3 Revision 7b working draft, January 1997

**Document:** *Information Technology — AT Attachment-3 Interface (ATA-3)*, **X3T13/2008D Revision 7b**, 27 January 1997.  
Inspected transcription/mirror: <https://paperzz.com/doc/7545036/at-attachment-3-interface--ata-3--working-draft>

The document identifies itself as a **working draft proposed American National Standard**, so this record does not silently call the inspected mirror a final normative facsimile. The recovered document identity, revision/date, revision history, clause numbering, and detailed command text are nevertheless sufficient for the bounded interface-semantic claims below.

### G1. Revision history records the July 1995 SFF8035i incorporation step

**Document Status, Revision 3 — 26 July 1995.**

The revision history records, under the July 18–20 working-group changes, `Added SFF8035i S.M.A.R.T. into the standard.`

This gives a period standards-history bridge from the SFF publication witness into the ATA-3 draft family. It does **not** establish the invention date of SMART, the first device implementation, or a complete revision-by-revision genealogy.

### G2. Attributes and thresholds are device-manufacturer policy/model state

**§6.6, especially §§6.6.1–6.6.4, printed pp. 35–36.**

The draft says SMART monitors and stores critical performance/calibration parameters to predict near-term degradation/fault conditions. It states that:

- attributes are selected by the device manufacturer;
- the specific set and identity of attributes are vendor-specific/proprietary;
- attribute values represent relative reliability;
- threshold values are determined by the manufacturer through design/reliability testing and analysis;
- an attribute value at or below its corresponding threshold makes the device reliability status indicate an impending degrading/fault condition.

This directly blocks two shortcuts:

`ATA SMART attribute set = one fixed cross-vendor physical-health schema` — unsupported;

`threshold crossed = exact failure instant` — unsupported; the historical wording is a predicted impending degrading/fault condition.

### G3. SMART enable state is retained control state

**§7.31.1 / §7.31.3, printed pp. 85–89.**

`SMART DISABLE OPERATIONS` says attribute values cease being monitored/saved while SMART is disabled, and that the SMART enabled/disabled state is preserved across power cycles. `SMART ENABLE OPERATIONS` likewise preserves that policy state and says repeated enabling does not alter the attribute values.

Therefore:

`SMART feature-policy state ≠ attribute value state`.

### G4. Autosave policy and attribute embodiment are separately retained

**§7.31.2, printed pp. 86–88.**

`SMART ENABLE/DISABLE ATTRIBUTE AUTOSAVE` may allow a device, after a vendor-specified event, to save updated attribute values to **nonvolatile memory**. The autosave enabled/disabled state is itself preserved across power cycles. Disabling autosave does not preclude saves during other normal operations such as power-on, power-off, or error recovery.

This supports the bounded decomposition:

`autosave policy ≠ autosave trigger/event ≠ saved attribute value`.

### G5. Reading/reporting can itself materialize updated health state nonvolatily

**§7.31.5, SMART READ ATTRIBUTE VALUES, printed p. 93; §7.31.6, SMART RETURN STATUS, printed p. 95; §7.31.7, SMART SAVE ATTRIBUTE VALUES, printed pp. 95–96.**

The draft says:

- `READ ATTRIBUTE VALUES` saves updated attribute values to nonvolatile memory before returning the 512-byte value structure;
- `RETURN STATUS` saves updated values to nonvolatile memory before comparing them against thresholds and reporting reliability status;
- `SAVE ATTRIBUTE VALUES` immediately writes updated values to nonvolatile memory regardless of the autosave timer.

The retention consequence is narrow but useful:

> host observation/status requests can be coupled to maintenance/materialization of the retained telemetry state itself.

This does not prove the physical NVRAM technology, update atomicity, wear policy, or exact manufacturer-specific attribute calculation.

### Provenance limit

The ATA-3 Revision 7b evidence used here is a third-party text mirror/transcription of a period X3T13 draft, not a directly rendered original committee facsimile in this run. The official T10 liaison PDF is the stronger archival anchor for the July 1995 SFF publication fact. A future slice should obtain and inspect original SFF-8035i and ATA-3 archival facsimiles before making finer priority or revision-wording claims.

'''
evidence = insert_before_once(
    evidence,
    '## Evidence ledger\n',
    prior_sources,
    'evidence source insertion',
)

evidence_rows = r'''| July 1995 SFF liaison record says a Quantum-submitted SMART copy was approved for publication as SFF-8035i | `H/P` | X3T10/95-292r0 p. 1 | strong official committee primary; publication floor only |
| ATA-3 Rev. 7b revision history says Rev. 3 (26 July 1995) added SFF8035i SMART | `H/P` | ATA-3 Rev. 7b Document Status | strong period draft text, mirror provenance |
| ATA SMART attribute identities are vendor-specific/proprietary and thresholds manufacturer-determined | `H/P` | ATA-3 §§6.6.1–6.6.4 | strong period draft semantics |
| ATA-3 SMART enabled/disabled state and autosave policy are preserved across power cycles | `H/P` | ATA-3 §§7.31.1–7.31.3 | strong period draft semantics |
| ATA-3 can save updated SMART attribute values to nonvolatile memory on autosave events or explicit read/status/save commands | `H/P` | ATA-3 §§7.31.2, 7.31.5–7.31.7 | strong period draft semantics |
| SFF-8035i approval or ATA-3 incorporation proves SMART invention priority | `X` | sources establish publication/incorporation only | rejected |
| ATA SMART attribute model is identical to NVMe SMART / Health fixed field schema | `X` | source contracts differ materially | rejected; functional/prior-art comparison only |
'''
evidence = replace_once(
    evidence,
    '| --- | --- | --- | --- |\n',
    '| --- | --- | --- | --- |\n' + evidence_rows,
    'evidence ledger rows',
)

prior_boundary = r'''## ATA prior-art boundary added in this pass

The new sources establish only a bounded historical floor:

```text
July 1995 SFF publication approval
        -> July 1995 ATA-3 revision-history incorporation marker
        -> January 1997 ATA-3 Rev. 7b retained-attribute/control semantics witness
        !=
SMART invention priority
        !=
complete SFF/ATA revision genealogy
        !=
direct ATA -> NVMe implementation descent
```

The comparison to NVMe is functional and interface-semantic. ATA-3's manufacturer-selected attribute/threshold model and NVMe's standardized named health fields both retain evidence about device condition/use, but `same label = SMART` is not evidence of identical schema, physical sensors, controller implementation, or historical continuity.

'''
evidence = insert_before_once(
    evidence,
    '## Related-repository check\n',
    prior_boundary,
    'evidence prior-art boundary',
)

evidence = replace_once(
    evidence,
    'A GitHub search of `tmzncty/computing-archaeology` for NVMe SMART / `Percentage Used` / P3700 endurance telemetry returned no dedicated case. Therefore no existing technical history was duplicated. If a broad history of SSD health monitoring, ATA SMART, JEDEC endurance methodology, or controller wear modeling is later written, it belongs primarily in `computing-archaeology`; this repository should retain the narrower state/history distinction.',
    'A fresh GitHub search of `tmzncty/computing-archaeology` for NVMe SMART / `Percentage Used` / P3700 endurance telemetry and ATA SMART / SFF-8035i returned no dedicated case. Therefore no existing technical history was duplicated. If a broad history of SMART, ATA drive diagnostics, SSD health monitoring, JEDEC endurance methodology, or controller wear modeling is later written, it belongs primarily in `computing-archaeology`; this repository should retain the narrower state/history and persistence-policy distinctions.',
    'evidence related repo update',
)

evidence = replace_once(
    evidence,
    'Future work should be separate slices: ATA SMART genealogy; JEDEC JESD218 methodology; independent calibration of `Percentage Used` against named-device physical wear/failure; modern NVMe telemetry/endurance-group extensions; and fleet-level replacement policy.',
    'Future work should be separate slices: direct SFF-8035i facsimile/revision archaeology; pre-SFF vendor SMART implementations; ATA-4/ATA-5 offline collection and self-test evolution; named-product SMART attribute meanings; JEDEC JESD218 methodology; independent calibration of `Percentage Used` against named-device physical wear/failure; modern NVMe telemetry/endurance-group extensions; and fleet-level replacement policy.',
    'evidence future work update',
)

# ---------------------------------------------------------------------------
# ROADMAP: mark only the bounded prior-art floor complete; keep the broad
# genealogy open.
# ---------------------------------------------------------------------------
roadmap_line = r'''- [x] ATA SMART retained-health-state prior-art floor for NVMe Case 55 — canonical [`cases/55-nvme-smart-health-endurance-telemetry.md`](cases/55-nvme-smart-health-endurance-telemetry.md), with [`evidence/55-nvme10-13-smart-health-endurance-grounding.md`](evidence/55-nvme10-13-smart-health-endurance-grounding.md), now adds the official July 1995 X3T10/SFF publication-approval witness for SFF-8035i plus January 1997 ATA-3 Revision 7b semantics for manufacturer-selected attributes/thresholds, nonvolatile attribute saves, and power-cycle-persistent SMART/autosave policy state. This closes only the bounded `drive-health state predates NVMe` / `same SMART label ≠ same schema` prior-art relation; direct SFF-8035i facsimile archaeology, pre-SFF vendor implementations, ATA-4/ATA-5 offline/self-test evolution, named-device attribute behavior, and any direct ATA→NVMe genealogy remain open and should be coordinated with `computing-archaeology`.

'''
roadmap = insert_before_once(
    roadmap,
    '- [x] SDRAM self-refresh transition-completion deepening',
    roadmap_line,
    'roadmap insertion',
)

# ---------------------------------------------------------------------------
# CASE_INDEX: append bounded findings after the current Case-103 tail.
# ---------------------------------------------------------------------------
index_add = r'''

## Case 55 ATA SMART prior-art deepening — retained health state before NVMe

1546. **NVMe SMART terminology ≠ NVMe origin of retained drive-health state** — July 1995 SFF committee evidence and the later ATA-3 draft establish an earlier standards-era regime in which a drive retained/qualified health information for host use.
1547. **SFF-8035i publication approval ≠ invention priority** — X3T10/95-292r0 says a Quantum-submitted SMART copy was approved for publication; that committee event does not identify the first concept, implementation, or inventor.
1548. **ATA-3 incorporation date ≠ first SMART implementation date** — the Revision 7b history says Revision 3 added SFF8035i SMART on 26 July 1995, but revision incorporation is a standards-history node rather than a product-origin certificate.
1549. **attribute value ≠ attribute threshold** — ATA-3 stores/returns relative-reliability values while manufacturer-set thresholds provide a separate comparison boundary for reliability status.
1550. **threshold crossed ≠ exact failure instant** — the ATA-3 wording is an impending degrading/fault condition, not a deterministic timestamp at which payload service must already have failed.
1551. **manufacturer-selected ATA attribute set ≠ standardized NVMe SMART / Health field schema** — shared health-monitoring purpose and the label `SMART` do not erase the difference between proprietary attribute identities and later named NVMe fields such as Available Spare and Percentage Used.
1552. **SMART enabled state ≠ monitored attribute value** — ATA-3 preserves whether SMART operations are enabled across power cycles while separately retaining/updating the values being monitored.
1553. **attribute-autosave policy ≠ autosave event ≠ nonvolatile attribute embodiment** — the policy may survive power cycles, a vendor-defined or other event may trigger saving, and the resulting attribute values are a third state relation.
1554. **autosave disabled ≠ attribute values can never be saved** — ATA-3 explicitly allows saves during other operations such as power-on/off or error recovery even when the optional autosave feature is disabled.
1555. **health-data read/status request ≠ purely passive observation** — ATA-3 READ ATTRIBUTE VALUES and RETURN STATUS can save updated values to nonvolatile memory before returning data/status, coupling observation to telemetry-state maintenance in the bounded interface.
1556. **nonvolatile health state ≠ user payload** — retained SMART attributes and control policy describe/qualify the device that carries user data; they are not the application data whose survival the device is serving.
1557. **retained attribute values ≠ complete device event history** — normalized/proprietary health values and threshold status compress observations and predictions rather than preserving every causal event, raw sensor sample, medium error, or chronological sequence.
1558. **power-cycle-persistent monitoring policy ≠ universally persistent warning state** — ATA-3 preserves SMART/autosave policy across power cycles while Case 55's NVMe 1.3 evidence explicitly makes `Critical Warning` current and nonpersistent; one health interface can retain different state classes under different persistence rules.
1559. **same `SMART` label across ATA and NVMe ≠ unchanged semantics or proven genealogy** — the comparison is a bounded prior-art/functional bridge, not evidence that the interfaces use identical sensors, state representation, failure model, or direct implementation descent.
'''
if '## Case 55 ATA SMART prior-art deepening — retained health state before NVMe' in index:
    raise RuntimeError('CASE_INDEX addition already present')
if not index.rstrip().endswith('1545. **SCSI VERIFY comparison ≠ historical genealogy among BMS, Patrol Read, scrub, or Consistency Check** — Cases 101–103 support a maintenance-locus comparison only; device, host, controller, and higher-layer verification regimes retain different vocabularies, authorities, and scopes.'):
    raise RuntimeError('CASE_INDEX tail moved; refusing to append against an unexpected base')
index = index.rstrip() + index_add + '\n'

# Normalize EOF and write.
for path, text in [
    (CASE_PATH, case),
    (EVIDENCE_PATH, evidence),
    (ROADMAP_PATH, roadmap),
    (INDEX_PATH, index),
]:
    path.write_text(text.rstrip() + '\n', encoding='utf-8')
