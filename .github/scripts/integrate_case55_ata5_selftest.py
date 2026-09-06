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
# Case 55: deepen the older ATA health-state floor with a bounded 1999
# ATA/ATAPI-5 diagnostic-history/self-test relation. Do not turn this into a
# full SMART genealogy.
# ---------------------------------------------------------------------------
case = replace_once(
    case,
    'A new prior-art pass adds a bounded 1995–1997 ATA SMART floor for retained drive-health state, while explicitly refusing to equate ATA vendor-specific attributes with the later NVMe SMART / Health schema or to claim a direct ATA→NVMe genealogy.',
    'A prior-art pass adds a bounded 1995–1997 ATA SMART floor for retained drive-health state, while explicitly refusing to equate ATA vendor-specific attributes with the later NVMe SMART / Health schema or to claim a direct ATA→NVMe genealogy. A further ATA/ATAPI-5 pass adds a bounded 1999 diagnostic-history relation: off-line data collection, short/extended self-test, off-line versus captive execution, current progress/status, and a finite circular self-test log are kept distinct.',
    'case status deepening',
)

historical_add = r'''### 1999 ATA/ATAPI-5 separates off-line data collection, self-test execution mode, and retained diagnostic history

The **ATA/ATAPI-5 Working Draft T13/1321D Revision 2, 13 December 1999** supplies a later but still pre-NVMe diagnostic-history boundary. This source is a period draft transcription/mirror rather than a directly rendered T13 facsimile; T13's official expired-standards ledger independently identifies project `1321D` as **AT Attachment - 5 with Packet Interface (ATA/ATAPI-5)** and gives its standards-submission date as **28 February 2000**. The December text is therefore used as a period working-draft witness, not silently promoted to the final published standard.

Its revision history is also useful but must not be mistaken for invention history. Revision `0c`, dated **5 March 1999**, records incorporation of `D99105R0 Self-test log modification` and `D99108R0 Optional pointer on self-test log`. T13's official 1999 document index independently lists those proposals as submitted on **10 February 1999** and **22 February 1999** respectively. This establishes an active 1999 standards-editing episode around self-test logging; it does **not** prove that SMART self-test or diagnostic logging originated in those proposals.

The substantive interface boundary appears in §8.41.4. `SMART EXECUTE OFF-LINE IMMEDIATE` can either collect SMART data in **off-line mode** and save it to device nonvolatile memory, or execute a **self-diagnostic test routine**. Table 34 gives separate subcommands for the SMART off-line routine, Short self-test, Extended self-test, abort, and captive-mode Short/Extended self-tests. The draft therefore does not support treating `off-line data collection` and `self-test` as synonyms.

The execution mode is a second independent axis. In **off-line mode**, command completion occurs **before** the subcommand routine runs; BSY remains clear/DRDY remains set, and an interrupting host command may suspend or abort the routine while still being serviced within two seconds. By contrast, in **captive mode** the device holds BSY while the self-test executes and completes the command only after recording the result. Short and Extended self-tests may use either mode.

This yields a historical interface decomposition:

```text
diagnostic/data-collection request
        -> selected routine
        -> execution mode (off-line or captive)
        -> current execution/progress state
        -> completion/result classification
        -> optional failure localization
        -> bounded retained self-test-log entry
```

The arrows are an **engineering reconstruction of documented relations**, not period terminology for one universal pipeline.

The retained-history boundary is especially explicit in §8.41.6.8.3. The SMART self-test log has **21 descriptor entries** and is a circular buffer: the twenty-second entry replaces the first. A descriptor retains the self-test subcommand, execution status, a `Life timestamp` measured as **device power-on lifetime in hours when that self-test completed**, a failure checkpoint, and a failing LBA when the failure was caused by an uncorrectable sector. If the test passed, or failed for another reason, the failing-LBA field is undefined.

Thus ATA/ATAPI-5 can retain evidence of the device's own diagnostic work, but the interface itself blocks several stronger readings: the log is bounded rather than exhaustive, its timebase is power-on lifetime rather than wall-clock chronology, and not every failed self-test has a meaningful media LBA.

'''
case = insert_before_once(
    case,
    '### NVMe 1.0 already separates spare threshold, spare exhaustion, and command failure\n',
    historical_add,
    'case ATA5 historical insertion',
)

engineering_add = r'''### Diagnostic trigger, execution mode, completion, verdict, and retained history are separate relations

ATA/ATAPI-5 adds a different kind of non-payload retained state to the earlier ATA-3 attribute/threshold model. The host can initiate a diagnostic routine, but what the command means cannot be reduced to a single `test happened` bit.

First, the draft separates the SMART off-line data-collection routine from Short/Extended self-tests. Second, it separates the **routine** from the **execution mode**: Short/Extended self-tests can run off-line or captive. Third, off-line command completion precedes diagnostic completion, while captive completion follows the test. Therefore:

> **SMART off-line data collection ≠ SMART self-test**,

> **self-test routine ≠ self-test execution mode**,

> **off-line command completion ≠ diagnostic completion**.

`Off-line` also does not mean that the device has become unavailable to the host. The documented off-line protocol keeps the command interface ready and requires many interrupting host commands to be serviced promptly, with the diagnostic work suspended, aborted, or later resumed depending on capability/policy. Therefore:

> **off-line diagnostic execution ≠ host-visible device offline/unavailable**.

The SMART READ DATA structure then keeps capability, progress, and outcome distinct. Separate bits report support for EXECUTE OFF-LINE IMMEDIATE, off-line read scanning, and Short/Extended self-test; the self-test execution byte separately reports approximate percent remaining and classifications such as completed, host-aborted, reset-interrupted, electrical failure, servo/seek failure, read failure, or in-progress. The recommended polling time is only a minimum recommendation before the host should first poll; the draft says actual test time may be several times that value.

Therefore:

> **off-line-data-collection capability ≠ off-line read-scan capability ≠ self-test capability**,

> **self-test progress/status ≠ final pass/fail verdict**,

> **host abort/reset interruption ≠ device-detected diagnostic failure**,

> **recommended polling time ≠ test-completion deadline**.

Finally, the 21-entry circular self-test log retains only a bounded diagnostic trace. It is not a complete event archive, and its `Life timestamp` is a power-on-hour coordinate rather than a civil-time timestamp. A failing LBA is meaningful only for the first uncorrectable sector that caused that particular test to fail; other failure classes need not yield such an address.

Therefore:

> **self-test log entry ≠ complete device event history**,

> **power-on-life timestamp ≠ wall-clock chronology**,

> **self-test failure ≠ universally localized failing LBA**.

This also provides a bounded functional comparison with Cases 101 and 103. ATA off-line self-test, SCSI Background Medium Scan, and host-issued SCSI VERIFY all qualify media/device condition while separating foreground service from maintenance in different ways. Their maintenance loci, triggering rules, scope, result records, and historical vocabularies differ, so the comparison does **not** establish an ATA↔SCSI genealogy.

'''
case = insert_before_once(
    case,
    '### The device can retain evidence about its own retention margin\n',
    engineering_add,
    'case ATA5 engineering insertion',
)

case = replace_once(
    case,
    '''It is **not** a full ATA SMART genealogy. The original SFF-8035i facsimile/revision chain, pre-SFF vendor implementations, ATA-4/ATA-5 changes, offline data collection/self-test evolution, named-product attribute meanings, and any direct ATA→NVMe design genealogy remain separate work. `SFF publication approval`, `ATA-3 incorporation`, and `invention` are not treated as synonyms.''',
    '''It is **not** a full ATA SMART genealogy. The original SFF-8035i facsimile/revision chain, pre-SFF vendor implementations, ATA-4 evolution, proposal-level facsimile archaeology for the 1999 self-test-log changes, later selective/conveyance self-test evolution, named-product diagnostic behavior, and any direct ATA→NVMe design genealogy remain separate work. The December 1999 ATA/ATAPI-5 Revision 2 text closes only a bounded diagnostic-history/interface relation; `proposal submission`, `working-draft incorporation`, `standards publication`, `first implementation`, and `invention` are not treated as synonyms.''',
    'case prior-art boundary update',
)

claim_rows = r'''| ATA/ATAPI-5 Revision 2 separates SMART off-line data collection from Short/Extended self-test and permits self-test in off-line or captive mode | `H/P` | strong period working-draft semantics; mirror provenance retained |
| Off-line mode completes the host command before the routine and can service interrupting host commands while the routine is suspended/aborted/resumed | `H/P` | strong period working-draft execution semantics |
| ATA/ATAPI-5 exposes separate current self-test progress/status and distinct capability bits for off-line immediate, off-line read scan, and self-test | `H/P` | strong period working-draft semantics |
| ATA/ATAPI-5 self-test history uses a 21-entry circular log with power-on-life completion timestamp and conditional failing-LBA field | `H/P` | strong period working-draft log semantics |
| 1999 T13 proposal/index and draft-revision evidence proves the invention of SMART self-test or direct ATA→NVMe genealogy | `X` | rejected; revision history is a standards-editing floor only |
'''
case = replace_once(
    case,
    '| --- | --- | --- |\n',
    '| --- | --- | --- |\n' + claim_rows,
    'case claim-ledger ATA5 rows',
)

case = replace_once(
    case,
    '8. X3T13, **AT Attachment-3 Interface (ATA-3), Working Draft X3T13/2008D Revision 7b**, 27 January 1997; period draft text/transcription used for §6.6 and §7.31 semantics and revision history: <https://paperzz.com/doc/7545036/at-attachment-3-interface--ata-3--working-draft>\n\n## Related repositories',
    '''8. X3T13, **AT Attachment-3 Interface (ATA-3), Working Draft X3T13/2008D Revision 7b**, 27 January 1997; period draft text/transcription used for §6.6 and §7.31 semantics and revision history: <https://paperzz.com/doc/7545036/at-attachment-3-interface--ata-3--working-draft>\n9. Technical Committee T13, **1999 document index**, official metadata for `d99105r0` (10 February 1999) and `d99108r0` (22 February 1999), plus the **Expired Standards** ledger identifying project 1321D / ATA/ATAPI-5 and its 28 February 2000 submission date: <https://t13.org/documents?created%5Bmax%5D=1999-12-31&created%5Bmin%5D=1999-01-01&order=field_document_number&page=1&sort=desc> and <https://www.t13.org/standards-expired>\n10. T13, **AT Attachment with Packet Interface - 5 (ATA/ATAPI-5), Working Draft T13/1321D Revision 2**, 13 December 1999; period draft transcription/mirror used for revision history and §§8.41.4–8.41.6: <https://studylib.net/doc/25730948/ata-atapi-5>\n\n## Related repositories''',
    'case sources ATA5 insertion',
)

case = replace_once(
    case,
    'A fresh repository search found no dedicated NVMe SMART/endurance or ATA SMART/SFF-8035i case in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology). Broader SMART/ATA/NVMe health-monitoring genealogy and disk/SSD engineering chronology should remain there if developed; this case keeps only the retention-specific state/history and interface-boundary distinctions.',
    'A fresh repository search found no dedicated NVMe SMART/endurance or ATA SMART/SFF-8035i/ATA5 self-test case in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology). Broader SMART/ATA/NVMe health-monitoring genealogy and disk/SSD engineering chronology should remain there if developed; this case keeps only the retention-specific state/history, diagnostic-history, and interface-boundary distinctions.',
    'case related-repo update',
)

# ---------------------------------------------------------------------------
# Evidence record: update the grounding question and append provenance-bounded
# Source H/I records. The T13 proposal PDFs are not claimed as inspected.
# ---------------------------------------------------------------------------
evidence = replace_once(
    evidence,
    'A new bounded prior-art pass adds an official July 1995 T10/SFF publication witness and a January 1997 ATA-3 working-draft semantics witness, establishing that retained drive-health state, threshold qualification, nonvolatile attribute saving, and power-cycle-persistent monitoring policy predate NVMe without claiming a complete SMART genealogy.',
    'A bounded prior-art pass adds an official July 1995 T10/SFF publication witness and a January 1997 ATA-3 working-draft semantics witness, establishing that retained drive-health state, threshold qualification, nonvolatile attribute saving, and power-cycle-persistent monitoring policy predate NVMe. A further 1999 ATA/ATAPI-5 pass grounds a different relation: device-initiated diagnostic work can be host-triggered yet asynchronous, expose separate capability/progress/result state, and leave a finite retained self-test history without becoming a complete device archive.',
    'evidence opening ATA5 update',
)

if '## Source H — T13 1999 SMART/self-test proposal metadata' in evidence:
    raise RuntimeError('evidence ATA5 sources already present')

evidence_add = r'''

## Source H — T13 1999 SMART/self-test proposal metadata

**Archive:** Technical Committee T13, 1999 document index.  
Official index: <https://t13.org/documents?created%5Bmax%5D=1999-12-31&created%5Bmin%5D=1999-01-01&order=field_document_number&page=1&sort=desc>

The official T13 index records, among other 1999 work items:

- `d99105r0`, **WD self-test log modification**, Hanmann, submitted **10 February 1999**;
- `d99108r0`, **Optional pointer for self-test log**, Evans, submitted **22 February 1999**;
- `d99104r0/r1/r2`, **Seagate SMART proposal**, with February–April 1999 submissions.

The proposal PDF bodies were **not directly inspected in this slice**. The archive metadata is therefore used only to establish that named self-test-log/SMART proposal artifacts existed at those dates. It does not support attributing detailed normative semantics to the proposals or claiming invention priority.

The ATA/ATAPI-5 Revision 2 history independently records that Revision `0c` on **5 March 1999** incorporated `D99105R0 Self-test log modification` and `D99108R0 Optional pointer on self-test log`. This is a standards-editing bridge, not an origin claim.

## Source I — ATA/ATAPI-5 T13/1321D Revision 2, 13 December 1999

**Document:** *Information Technology — AT Attachment with Packet Interface - 5 (ATA/ATAPI-5)*, Working Draft **T13/1321D Revision 2**, **13 December 1999**.  
Inspected transcription/mirror: <https://studylib.net/doc/25730948/ata-atapi-5>  
Official T13 project/date corroboration: <https://www.t13.org/standards-expired>

The draft identifies itself as an **internal working document** rather than a completed standard. T13's official expired-standards page independently identifies project `1321D` as ATA/ATAPI-5 and gives **28 February 2000** as its standards-submission date. Accordingly, the detailed clause semantics below are cited to the December 1999 working draft, not misdescribed as final-publication wording.

### I1. Off-line data collection and self-test are distinct subcommands

**§8.41.4.8, Table 34, printed p. 194.**

`SMART EXECUTE OFF-LINE IMMEDIATE` is described as either initiating activities that collect SMART data in off-line mode and save it to device nonvolatile memory, **or** executing a self-diagnostic routine. Table 34 separately enumerates:

- SMART off-line routine in off-line mode;
- Short self-test in off-line mode;
- Extended self-test in off-line mode;
- abort off-line self-test;
- Short self-test in captive mode;
- Extended self-test in captive mode.

Directly supported boundary:

`SMART off-line data collection ≠ SMART Short/Extended self-test`.

### I2. Off-line command completion precedes diagnostic completion

**§8.41.4.8.1, printed pp. 194–195.**

In off-line mode the device completes the command **before** executing the subcommand routine, keeps BSY clear/DRDY set, and may suspend or abort the routine to service a new host command within two seconds. Depending on capability/policy it may later re-initiate or resume the routine without another host request.

Directly supported boundaries:

`command completion ≠ diagnostic completion`;

`off-line execution ≠ host-visible device unavailability`;

`host command arrival ≠ necessarily permanent diagnostic abandonment`.

### I3. Captive/off-line is an execution-mode distinction, not a separate Short/Extended objective

**§§8.41.4.8.2–8.41.4.8.5, printed p. 195.**

Captive mode holds BSY during the self-test and performs command completion after placing the result in the self-test execution-status byte. Short and Extended self-tests can instead be selected in either captive or off-line mode.

Therefore:

`self-test routine/objective ≠ execution mode`.

### I4. Capability, progress, interruption, and failure classification are separate fields

**§§8.41.5.8.2–8.41.5.8.6, printed pp. 198–199.**

The self-test execution-status byte contains approximate percent remaining in ten-percent increments and separately classifies states including completed/no previous test, host-aborted, reset-interrupted, fatal/unknown error, failed electrical element, failed servo/seek element, failed read element, and in-progress.

The off-line capability byte separately distinguishes implementation of EXECUTE OFF-LINE IMMEDIATE, off-line read scanning, and Short/Extended self-test, while bit 2 defines abort-versus-suspend/resume behavior on an interrupting host command.

The recommended polling time is explicitly only the minimum recommended interval before the host should first poll; actual test time may be several times longer, and early polling can itself alter execution depending on bit 2.

Directly supported boundaries:

`capability ≠ progress ≠ result`;

`host abort/reset interruption ≠ device-detected self-test failure`;

`recommended polling interval ≠ completion deadline`.

### I5. The retained self-test history is finite and overwriting

**§8.41.6.8.3, Tables 45–46, printed pp. 205–206.**

The SMART self-test log contains **21 descriptor entries** and is defined as a circular buffer: entry 22 replaces entry 1, entry 23 replaces entry 2, and so on.

Each descriptor records the issued self-test subcommand, completion execution status, a `Life timestamp`, failure checkpoint, failing LBA, and vendor-specific bytes. The `Life timestamp` is the **device power-on lifetime in hours when that self-test completed**.

The failing-LBA field is only defined when an uncorrectable sector caused the test to fail; it records the first such LBA. If the test passed, or failed for another reason, the field is undefined.

Directly supported boundaries:

`retained self-test log ≠ complete lifetime event archive`;

`power-on-life timestamp ≠ wall-clock timestamp`;

`self-test failure ≠ universally localized media-sector failure`.

### Provenance and priority limit

The 1999 T13 document index is an official committee archive for proposal metadata. The detailed ATA/ATAPI-5 clauses used here come from a period draft transcription/mirror whose document identity, revision/date, page structure, and revision history are internally explicit and independently consistent with T13 project metadata. This slice does **not** claim direct visual inspection of the original proposal PDFs or a final ATA/ATAPI-5 facsimile, does not establish the first implementation of SMART self-test, and does not infer a direct implementation genealogy from ATA into NVMe or SCSI.
'''
evidence = evidence.rstrip() + evidence_add + '\n'

# ---------------------------------------------------------------------------
# ROADMAP: advance the exact open ATA-4/ATA-5 self-test slice without closing
# full SMART genealogy or named-product validation.
# ---------------------------------------------------------------------------
roadmap_old = '- [x] ATA SMART retained-health-state prior-art floor for NVMe Case 55 — canonical [`cases/55-nvme-smart-health-endurance-telemetry.md`](cases/55-nvme-smart-health-endurance-telemetry.md), with [`evidence/55-nvme10-13-smart-health-endurance-grounding.md`](evidence/55-nvme10-13-smart-health-endurance-grounding.md), now adds the official July 1995 X3T10/SFF publication-approval witness for SFF-8035i plus January 1997 ATA-3 Revision 7b semantics for manufacturer-selected attributes/thresholds, nonvolatile attribute saves, and power-cycle-persistent SMART/autosave policy state. This closes only the bounded `drive-health state predates NVMe` / `same SMART label ≠ same schema` prior-art relation; direct SFF-8035i facsimile archaeology, pre-SFF vendor implementations, ATA-4/ATA-5 offline/self-test evolution, named-device attribute behavior, and any direct ATA→NVMe genealogy remain open and should be coordinated with `computing-archaeology`.'
roadmap_new = '- [x] ATA SMART retained-health-state and ATA/ATAPI-5 diagnostic-history prior-art floor for NVMe Case 55 — canonical [`cases/55-nvme-smart-health-endurance-telemetry.md`](cases/55-nvme-smart-health-endurance-telemetry.md), with [`evidence/55-nvme10-13-smart-health-endurance-grounding.md`](evidence/55-nvme10-13-smart-health-endurance-grounding.md), retains the official July 1995 X3T10/SFF publication-approval witness and January 1997 ATA-3 attribute/persistence semantics, and now adds the December 1999 ATA/ATAPI-5 Revision 2 boundary separating off-line data collection, Short/Extended self-test, off-line/captive execution, asynchronous command completion, current progress/result state, and a finite 21-entry circular self-test history. Official T13 metadata also grounds the February–March 1999 self-test-log proposal/incorporation episode without treating revision history as invention history. This closes only the bounded `drive-health state predates NVMe` / `diagnostic history is finite retained state` relation; original SFF-8035i and 1999 proposal facsimile archaeology, pre-SFF vendor implementations, ATA-4 evolution, later selective/conveyance self-test genealogy, named-device diagnostic behavior, and any direct ATA→NVMe genealogy remain open and should be coordinated with `computing-archaeology`.'
roadmap = replace_once(roadmap, roadmap_old, roadmap_new, 'ROADMAP Case55 ATA SMART item')

# ---------------------------------------------------------------------------
# CASE_INDEX: append findings after the current 1559 endpoint. This is a
# deepening of Case55, not a new case or maturity change.
# ---------------------------------------------------------------------------
if '## Case 55 ATA/ATAPI-5 SMART self-test deepening' in index:
    raise RuntimeError('CASE_INDEX ATA5 section already present')
if '1559. **same `SMART` label across ATA and NVMe ≠ unchanged semantics or proven genealogy**' not in index:
    raise RuntimeError('CASE_INDEX expected 1559 endpoint not found')

index_add = r'''

## Case 55 ATA/ATAPI-5 SMART self-test deepening — retained diagnostic history and asynchronous qualification

1560. **SMART off-line data collection ≠ SMART self-test** — ATA/ATAPI-5 Table 34 assigns distinct subcommands to the SMART off-line routine and to Short/Extended self-tests; a shared command family does not collapse their purposes.
1561. **off-line execution mode ≠ host-visible device unavailability** — in the 1999 draft, off-line mode clears BSY/sets DRDY and can service interrupting host commands while diagnostic work is suspended, aborted, or later resumed.
1562. **off-line command completion ≠ diagnostic completion** — ATA/ATAPI-5 explicitly completes the command before executing an off-line subcommand routine, so foreground command success is not a completion certificate for the later diagnostic work.
1563. **self-test routine/objective ≠ self-test execution mode** — Short/Extended self-tests may run either off-line or captive; captive/off-line changes service/completion semantics rather than defining a different Short/Extended diagnostic objective.
1564. **host abort/reset interruption ≠ device-detected self-test failure** — the self-test status byte distinguishes host abort and reset interruption from fatal/unknown, electrical, servo/seek, and read-element failures.
1565. **self-test progress/status ≠ final pass/fail verdict** — the same status structure carries approximate percent remaining and an in-progress state alongside terminal classifications.
1566. **off-line-data-collection capability ≠ off-line read-scan capability ≠ self-test capability** — ATA/ATAPI-5 assigns separate capability bits to these functions rather than one generic `SMART testing` capability.
1567. **recommended polling time ≠ test-completion deadline** — the draft calls the field a minimum recommendation for first polling, states actual test time may be several times longer, and warns that early polling may change execution behavior.
1568. **self-test log entry ≠ complete device event history** — the ATA/ATAPI-5 self-test log retains only 21 descriptor entries and overwrites old entries circularly.
1569. **power-on-life timestamp ≠ wall-clock chronology** — a self-test descriptor records device power-on lifetime in hours at completion, not a civil/calendar timestamp.
1570. **self-test failure ≠ universal fault localization** — the failing-LBA field is defined for the first uncorrectable sector causing failure and is undefined for a passing test or failures from other causes.
1571. **1999 proposal/incorporation evidence ≠ invention priority** — official T13 proposal metadata plus the Revision 0c incorporation ledger establish a standards-editing episode around self-test logging, not the first concept, first product implementation, or inventor.
1572. **ATA off-line self-test ≠ SCSI BMS ≠ host SCSI VERIFY** — Cases 55, 101, and 103 support a bounded maintenance-locus/qualification analogy, but different triggers, scopes, execution contracts, and retained result state do not establish historical genealogy.
'''
index = index.rstrip() + index_add + '\n'

for path, text in (
    (CASE_PATH, case),
    (EVIDENCE_PATH, evidence),
    (ROADMAP_PATH, roadmap),
    (INDEX_PATH, index),
):
    path.write_text(text.rstrip() + '\n', encoding='utf-8')
