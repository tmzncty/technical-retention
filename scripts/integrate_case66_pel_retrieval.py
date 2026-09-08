from pathlib import Path
import re

CASE = Path('cases/66-nvme14-persistent-event-log-history.md')
EVIDENCE = Path('evidence/66-nvme14-2019-persistent-event-log-grounding.md')
ROADMAP = Path('ROADMAP.md')
INDEX = Path('CASE_INDEX.md')

CASE_MARKER = '## 2021 implementation and reporting-generation deepening'
EVIDENCE_MARKER = '## 2021 deepening — implementation artifacts and retrieval-generation validation'
ROADMAP_MARKER = 'NVMe PEL retrieval-validity / reporting-generation deepening'
INDEX_MARKER = '### Case 66 deepening — PEL implementation and retrieval-validity findings'


def append_once(path: Path, marker: str, block: str) -> None:
    text = path.read_text(encoding='utf-8')
    if marker in text:
        return
    path.write_text(text.rstrip() + '\n\n' + block.strip() + '\n', encoding='utf-8')


case_block = r'''
## 2021 implementation and reporting-generation deepening

The original Case 66 boundary remains the ratified NVMe 1.4 PEL contract of 10 June 2019. This section adds **later implementation evidence and post-1.4 retrieval-validity evolution** without projecting those later rules backward into the 2019 standard.

### 2019 host tooling exposed support and size before a full PEL decoder landed

Two `linux-nvme/nvme-cli` commits dated **25 August 2019** added host-side Identify Controller visibility for the new NVMe 1.4 PEL surface:

- `81b5524bc887cb63447f5acbe41bb128bf62cb8c` — `id-ctrl: show Persistent Event Log Size(PELS)`;
- `cf98706f0051d44cea4e72abc43c78555040e77b` — `id-ctrl: show Persistent Event Log support in LPA`.

These are primary implementation-history artifacts for the Linux NVMe tooling ecosystem. They show that software could expose whether a controller advertised PEL support and its maximum log size shortly after NVMe 1.4 was ratified.

They do **not** prove that the tool could yet reconstruct the complete event population, that any named controller obeyed the cross-reset persistence requirement, or that 25 August 2019 is the origin date of PEL. The normative mechanism remains grounded in the earlier NVMe 1.4 standard.

Therefore:

> **advertised PEL support / size ≠ demonstrated PEL retrieval correctness.**

### January 2021 adds a full host-side PEL retrieval/parser path

On **11 January 2021**, `linux-nvme/nvme-cli` commit `6879ac41fcc62c468452a8c3e18c60c41e7eac62` added support for Persistent Event Log Page retrieval and decoding, explicitly citing NVMe 1.4 §5.14.1.13 and its cross-power/reset persistence contract.

This is useful implementation evidence because it establishes a concrete host software path from the standardized log to operator-visible event history. It is still not device-conformance evidence:

> **host parser implementation ≠ controller implementation or conformance.**

The host can know the wire format and still encounter controller-specific unsupported events, malformed data, tool bugs, or transfer-consistency problems.

### A November 2021 parser fix contains a named Samsung PM1735 retrieval artifact

Commit `d7c2dd59633fb0485edb5f6093d87154b19ace72`, dated **11 November 2021**, fixes a crash/misparse in the PEL path and includes an actual command/output artifact from a Samsung **PM1735**, reported as `PCIe4 1.6TB NVMe Flash Adapter x8`. The captured header shows a nontrivial PEL population and then demonstrates the parser losing event boundaries and producing implausible event types before the fix.

This is deliberately used at a narrow level:

- it is a **named hardware/tooling retrieval witness**;
- it proves that a real PM1735 exposed enough PEL data for the Linux tool to parse and fail on it;
- it does **not** prove cross-power-cycle persistence by controlled test;
- it does **not** prove that every PEL field/event on that drive conforms to every NVMe 1.4 requirement;
- it does **not** reveal the physical medium or controller metadata layout used to retain PEL entries.

The artifact supplies an important retention boundary:

> **underlying event-history presence ≠ correct host reconstruction of that history.**

A software decoding failure can make retained history operationally illegible without establishing that the controller forgot the history itself.

### NVMe 2.0a makes multi-command retrieval validity explicitly checkable

The ratified **NVM Express Base Specification Revision 2.0a**, dated **26 July 2021**, adds an explicit `Generation Number` and reporting-context information to the PEL header. For a PEL not read in one Get Log Page command, the host is instructed to:

1. establish a reporting context;
2. read the Generation Number before collecting the remainder of the log;
3. read the log through that context;
4. reread the Generation Number after the entire transfer;
5. reread the log if the two generation numbers do not match.

Revision 2.0a says a mismatch means the reporting context **may have been lost**, the collected PEL contents **may be invalid**, and host software should reread the log. The Generation Number increments when a reporting context is established and the log page returns data different from the previous reporting context, with defined rollover behavior.

Two `nvme-cli` commits dated **15 November 2021** implement this later contract:

- `303e03c6e228f9296b2fa70ec899db620f2e10f6` — verifies the Generation Number around a multi-command PEL collection and rereads on inconsistency;
- `82ea68f15b5b5bb0426dc28185fee07baa3729bb` — adds the NVMe 2.0a Generation Number and Reporting Context Information fields.

This creates a stronger distinction than the original 2019 case could establish:

> **persistent log ≠ valid retrieved image.**

> **successful chunk transfers ≠ one coherent historical view.**

> **reporting-context establishment ≠ proof that the same context survived the complete retrieval.**

The later Generation Number is a validation relation over the **host's recovered view** of retained history. It is not itself the event history and it is not evidence that every event has been preserved indefinitely.

### Generation mismatch is not itself proof of event loss

The NVMe 2.0a wording is intentionally conditional: when the numbers differ, the context may have been lost and the contents may be invalid. That does not establish which event entries physically disappeared, whether the underlying PEL changed legitimately, or whether the host merely crossed reporting contexts during retrieval.

Therefore:

> **retrieval-generation mismatch ≠ proven event erasure.**

and conversely:

> **matching generation ≠ archival completeness.**

A matching generation qualifies one collected image as belonging to one stable reporting generation. The separate NVMe 1.4/2.0a capacity, suppression, deletion, sanitize, and supported-event rules still bound what history can exist in that image.

### Reporting-context loss and PEL loss remain different failure classes

Case 66 already separated the temporary reporting context from the longer-lived PEL. The 2.0a Generation Number makes that separation operationally testable:

```text
persistent event population
    != temporary reporting context
    != reporting-generation validation token
    != host transfer buffers
    != decoded operator-visible history
```

A controller reset can invalidate the reporting context while the PEL's cross-reset retention contract still applies to event information. Host software then has reconstruction work to do again. This is not media repair; it is **re-establishment and validation of a retrieval relation**.

### Cross-case boundary: Case 90 is analogy, not genealogy

Case 90's later Kafka leader-epoch history shows a different system in which retained recovery metadata may physically exist yet be incomplete or ineligible for the recovery decision being attempted. The useful comparison is only functional:

> **retained metadata presence ≠ metadata admissibility for a particular recovery/retrieval operation.**

PEL Generation Number validation and Kafka leader-epoch admissibility are not the same mechanism, do not share a demonstrated lineage, and operate at different layers.

### Related-repository boundary

A fresh repository search in this round found no dedicated NVMe Persistent Event Log case in `tmzncty/computing-archaeology`. The broad ATA/SCSI/NVMe diagnostic-log genealogy, device-controller architecture, and physical firmware implementation remain better candidates for that companion repository. Case 66 keeps only the retention-specific lifetime, selection, retrieval, and validity relations.

## Sources added in this deepening

1. NVM Express, Inc., **NVM Express Base Specification Revision 2.0a**, 26 July 2021, Persistent Event Log reporting-context / Generation Number provisions: <https://nvmexpress.org/wp-content/uploads/NVMe-NVM-Express-2.0a-2021.07.26-Ratified.pdf>
2. `linux-nvme/nvme-cli`, `81b5524bc887cb63447f5acbe41bb128bf62cb8c`, **“id-ctrl: show Persistent Event Log Size(PELS)”**, 25 August 2019: <https://github.com/linux-nvme/nvme-cli/commit/81b5524bc887cb63447f5acbe41bb128bf62cb8c>
3. `linux-nvme/nvme-cli`, `cf98706f0051d44cea4e72abc43c78555040e77b`, **“id-ctrl: show Persistent Event Log support in LPA”**, 25 August 2019: <https://github.com/linux-nvme/nvme-cli/commit/cf98706f0051d44cea4e72abc43c78555040e77b>
4. `linux-nvme/nvme-cli`, `6879ac41fcc62c468452a8c3e18c60c41e7eac62`, **“nvme: add support for persistent event log page”**, 11 January 2021: <https://github.com/linux-nvme/nvme-cli/commit/6879ac41fcc62c468452a8c3e18c60c41e7eac62>
5. `linux-nvme/nvme-cli`, `d7c2dd59633fb0485edb5f6093d87154b19ace72`, **“libnvme: core dump when running nvme persistent-event-log”**, 11 November 2021: <https://github.com/linux-nvme/nvme-cli/commit/d7c2dd59633fb0485edb5f6093d87154b19ace72>
6. `linux-nvme/nvme-cli`, `303e03c6e228f9296b2fa70ec899db620f2e10f6`, **“nvme: PEL need to check gen number for verification of collected log”**, 15 November 2021: <https://github.com/linux-nvme/nvme-cli/commit/303e03c6e228f9296b2fa70ec899db620f2e10f6>
7. `linux-nvme/nvme-cli`, `82ea68f15b5b5bb0426dc28185fee07baa3729bb`, **“Add New fields on PEL based on NVMe 2.0a”**, 15 November 2021: <https://github.com/linux-nvme/nvme-cli/commit/82ea68f15b5b5bb0426dc28185fee07baa3729bb>
'''


evidence_block = r'''
## 2021 deepening — implementation artifacts and retrieval-generation validation

### Purpose

This addendum does **not** change the original 2019 mechanism boundary. It adds later primary implementation artifacts and the ratified NVMe 2.0a retrieval-validation rules in order to test a narrower proposition:

> cross-reset persistence of the underlying PEL is not by itself sufficient to guarantee that a host has reconstructed one coherent historical image.

The sources are used as **post-1.4 evolution and implementation evidence**, never as wording that is retroactively attributed to NVMe 1.4.

### P5 — NVM Express Base Specification Revision 2.0a (26 July 2021)

Primary normative source:

<https://nvmexpress.org/wp-content/uploads/NVMe-NVM-Express-2.0a-2021.07.26-Ratified.pdf>

Directly inspected PEL material includes the reporting-context sequence and the PEL header fields on the printed pages around 200–202.

Verified facts:

- a multi-command PEL retrieval has a reporting context;
- if the PEL is not read with one command, the host should inspect the `Generation Number` after establishing the context and again after completing the log read;
- if the numbers do not match, the reporting context may have been lost, the collected PEL contents may be invalid, and host software should reread the log;
- the PEL header includes `Generation Number` and `Reporting Context Information`;
- Generation Number changes when a newly established reporting context would return different log-page data than the previous reporting context and has defined rollover behavior.

Safe claims:

- `persistent PEL != automatically valid host-collected image`;
- `successful component transfers != verified one-generation retrieval`;
- the later protocol provides host-visible validation state for a multi-command historical view.

Unsafe upgrades:

- Generation Number proves every event is present;
- a mismatch proves physical loss of PEL entries;
- these 2.0a fields were already part of the exact 2019 Revision-1.4 contract.

### P6 — Linux nvme-cli Identify support, 25 August 2019

Primary implementation-history artifacts:

- `81b5524bc887cb63447f5acbe41bb128bf62cb8c`, `id-ctrl: show Persistent Event Log Size(PELS)`: <https://github.com/linux-nvme/nvme-cli/commit/81b5524bc887cb63447f5acbe41bb128bf62cb8c>
- `cf98706f0051d44cea4e72abc43c78555040e77b`, `id-ctrl: show Persistent Event Log support in LPA`: <https://github.com/linux-nvme/nvme-cli/commit/cf98706f0051d44cea4e72abc43c78555040e77b>

These commits establish a dated Linux-host-tooling floor for exposing PEL capability and size after NVMe 1.4.

They do not establish full PEL retrieval, device conformance, or invention priority.

### P7 — Linux nvme-cli PEL decoder, 11 January 2021

Primary implementation artifact:

`6879ac41fcc62c468452a8c3e18c60c41e7eac62`, `nvme: add support for persistent event log page`:

<https://github.com/linux-nvme/nvme-cli/commit/6879ac41fcc62c468452a8c3e18c60c41e7eac62>

The commit explicitly cites NVMe 1.4 §5.14.1.13, implements retrieval of Log Identifier `0Dh`, and adds decoding for multiple standardized PEL event types.

Safe claim:

> by January 2021, a concrete Linux userspace implementation existed for retrieving/decoding the standardized PEL.

Unsafe claim:

> this commit proves all compliant controllers retained every PEL event correctly.

### P8 — named Samsung PM1735 retrieval/parser artifact, 11 November 2021

Primary implementation/debug artifact:

`d7c2dd59633fb0485edb5f6093d87154b19ace72`, `libnvme: core dump when running nvme persistent-event-log`:

<https://github.com/linux-nvme/nvme-cli/commit/d7c2dd59633fb0485edb5f6093d87154b19ace72>

The commit message includes captured PEL output for a Samsung PM1735 identified as `PCIe4 1.6TB NVMe Flash Adapter x8`, followed by incorrect parser results and a crash/misparse diagnosis.

Evidence strength:

- strong for a **named hardware/tooling interaction** in 2021;
- useful for proving that retained structured device history can become unusable at the host parser layer;
- insufficient for a controlled cross-power retention test;
- insufficient for whole-device NVMe compliance or physical PEL-layout claims.

Safe reconstruction:

> **host-side historical legibility can fail while the device still presents a PEL structure.**

This is not evidence that the device forgot the event history.

### P9 — Linux nvme-cli Generation Number verification, 15 November 2021

Primary implementation artifacts tied explicitly to the later NVMe 2.0a contract:

- `303e03c6e228f9296b2fa70ec899db620f2e10f6`, `nvme: PEL need to check gen number for verification of collected log`: <https://github.com/linux-nvme/nvme-cli/commit/303e03c6e228f9296b2fa70ec899db620f2e10f6>
- `82ea68f15b5b5bb0426dc28185fee07baa3729bb`, `Add New fields on PEL based on NVMe 2.0a`: <https://github.com/linux-nvme/nvme-cli/commit/82ea68f15b5b5bb0426dc28185fee07baa3729bb>

The first commit restates the multi-command Generation Number check and the consequences of mismatch; the second adds the later header fields.

These are especially useful because they bridge normative retrieval-validity semantics to an independently inspectable host implementation.

### Claim ledger — 2021 deepening

| Claim | Layer | Support | Boundary |
| --- | --- | --- | --- |
| nvme-cli exposed PEL support and PELS in August 2019 | `H/P` | P6 | host tooling, not device conformance |
| nvme-cli added PEL retrieval/decoding in January 2021 | `H/P` | P7 | implementation floor, not invention date |
| a Samsung PM1735 appears in a November 2021 PEL parser/debug artifact | `H/P` | P8 | named retrieval witness, not controlled cross-power test |
| parser failure can make retained history operationally illegible without proving device-side loss | `E` | P8 | host reconstruction failure only |
| NVMe 2.0a adds Generation Number / Reporting Context Information to qualify multi-command PEL retrieval | `H/P` | P5 | later standard; do not back-project into 1.4 |
| matching generation qualifies one retrieval generation, not completeness of all historical events | `E` | P5 + original PEL capacity/suppression rules | completeness remains separately bounded |
| generation mismatch means retrieval may be invalid/context lost, not that event erasure is proven | `H/P` + `E` | P5 | preserve conditional normative wording |
| reporting-context failure and persistent-log loss are different failure classes | `E` | P5 + original 1.4 context/persistence rules | internal controller representation remains unknown |
| PEL retrieval-validity and Kafka epoch-cache admissibility are only functional analogies | `A`, `X` | Case 90 comparison | no shared genealogy/mechanism claimed |

### Updated evidence debt

This deepening closes two earlier gaps only partially:

- **named-device implementation evidence:** now there is a named PM1735 host-tooling retrieval artifact, but no controlled power-cycle/reset conformance trace;
- **later NVMe evolution:** NVMe 2.0a retrieval-generation validation is now grounded, but later revisions and implementation-specific edge cases remain open.

Still open:

- physical PEL storage/layout inside real controllers;
- exact power-failure atomicity of individual event creation;
- controlled before/after power-cycle event-retention traces on named drives;
- independent malformed/context-loss fault injection;
- exact sanitize-time event-removal behavior on named devices;
- ATA/SCSI and broader device-history genealogy.
'''


append_once(CASE, CASE_MARKER, case_block)
append_once(EVIDENCE, EVIDENCE_MARKER, evidence_block)

# Update the Case 66 table row in the authoritative index.
index_text = INDEX.read_text(encoding='utf-8')
lines = index_text.splitlines()
for i, line in enumerate(lines):
    if '(cases/66-nvme14-persistent-event-log-history.md)' in line:
        line = line.replace('expanded 2011–2019 NVMe log-lifetime/PEL grounding', 'expanded 2011–2021 NVMe log-lifetime/PEL/retrieval-validity grounding')
        line = line.replace('ATA/SCSI genealogy, named-device implementation/compliance, physical PEL layout, later NVMe evolution, and failure-injection validation remain separate work', 'ATA/SCSI genealogy, named-device cross-reset compliance, physical PEL layout, post-2.0a evolution, and failure-injection validation remain separate work')
        lines[i] = line
        break
else:
    raise SystemExit('Case 66 table row not found')
index_text = '\n'.join(lines).rstrip() + '\n'

if INDEX_MARKER not in index_text:
    nums = [int(x) for x in re.findall(r'^- \*\*(\d+) —', index_text, flags=re.M)]
    if not nums:
        raise SystemExit('No numbered findings found')
    start = max(nums) + 1
    findings = [
        ('2019 PEL standardization ≠ 2019 full host-tool support', 'NVMe 1.4 is the normative mechanism floor; August-2019 nvme-cli Identify additions expose capability/size while the full retrieval/decoder path appears later. (`H/P`, `X`)'),
        ('advertised PEL support/size ≠ demonstrated retrieval correctness', 'LPA/PELS can describe the interface while host decoding, context handling, or device behavior still requires separate validation. (`H/P`, `E`)'),
        ('host parser implementation ≠ controller conformance', 'the January-2021 nvme-cli decoder establishes a concrete software path, not proof that any controller obeys every persistence/event requirement. (`H/P`, `X`)'),
        ('named PM1735 PEL retrieval artifact ≠ controlled cross-power retention test', 'the November-2021 debug trace is a named hardware/tooling witness but does not compare event populations across reset/power cycles. (`H/P`, `X`)'),
        ('parser failure ≠ underlying event-history absence', 'the PM1735 artifact demonstrates that host reconstruction can become nonsensical/crash while a structured PEL is still being returned. (`H/P`, `E`)'),
        ('persistent log ≠ valid retrieved image', 'NVMe 2.0a Generation Number validation makes the host-collected historical image a separately qualified relation. (`H/P`, `E`)'),
        ('successful chunk transfers ≠ coherent multi-command history', 'individual Get Log Page transfers can complete while a changed/lost reporting context makes the aggregate image invalid. (`H/P`, `E`)'),
        ('reporting-context establishment ≠ proof of context survival through retrieval', 'the later standard explicitly requires before/after Generation Number checking for a multi-command read. (`H/P`, `E`)'),
        ('generation mismatch ≠ proven event erasure', 'NVMe 2.0a says the context may have been lost and contents may be invalid; it does not identify which underlying PEL entries physically disappeared. (`H/P`, `E`, `X`)'),
        ('matching generation ≠ archival completeness', 'one generation validates retrieval coherence while capacity, suppression, deletion, sanitize, and unsupported-event rules still bound historical coverage. (`H/P`, `E`)'),
        ('reporting-context loss ≠ persistent-log loss', 'temporary retrieval state can be invalidated while the separate cross-reset PEL event-retention contract remains in force. (`H/P`, `E`)'),
        ('host reread/re-establishment ≠ media repair', 'rebuilding a valid view after context loss repairs the retrieval relation, not the underlying NAND payload or event-record medium. (`E`)'),
        ('NVMe 2.0a retrieval validation ≠ NVMe 1.4 shipped semantics', 'the July-2021 Generation Number/RCI rules are later evolution and must not be projected into the exact June-2019 contract. (`H/P`, `X`)'),
        ('historical-detail retention lifetime ≠ retrieval-view validity lifetime', 'PEL entries may outlive the temporary context and one host transfer, so preservation and legibility have distinct temporal failure boundaries. (`H/P`, `E`)'),
        ('PEL retrieval validity ≠ Kafka leader-epoch metadata admissibility', 'both demonstrate that retained state may need a validity relation before use, but the similarity is functional only and does not establish one mechanism or genealogy. (`A`, `X`)'),
        ('related-repository boundary', 'current `tmzncty/computing-archaeology` search still found no dedicated NVMe PEL case; broad ATA/SCSI/NVMe diagnostic-log and controller genealogy belongs there if developed. (`H/P` project-state record)'),
    ]
    section = ['','### Case 66 deepening — PEL implementation and retrieval-validity findings','']
    for offset, (title, body) in enumerate(findings):
        section.append(f'- **{start + offset} — {title}:** {body}')
    index_text = index_text.rstrip() + '\n' + '\n'.join(section) + '\n'
INDEX.write_text(index_text, encoding='utf-8')

# Put this bounded completed slice at the top of Phase 2 so status is visible without disturbing older entries.
roadmap_text = ROADMAP.read_text(encoding='utf-8')
if ROADMAP_MARKER not in roadmap_text:
    phase = '## Phase 2 — Build missing technical bridges\n\n'
    if phase not in roadmap_text:
        raise SystemExit('Phase 2 marker not found')
    item = ('- [x] NVMe PEL retrieval-validity / reporting-generation deepening — canonical Case 66 and Evidence 66 now add August-2019 nvme-cli capability/size exposure, January-2021 host retrieval/decoding, a November-2021 named Samsung PM1735 parser/debug artifact, and the ratified 26 July 2021 NVMe 2.0a Generation Number / Reporting Context Information rules for validating multi-command PEL collection. This closes only the bounded `persistent event population vs temporary reporting context vs retrieval-generation validation vs decoded host history` relation; it does not turn the named-drive artifact into a cross-power conformance test, back-project 2.0a semantics into 1.4, or close physical PEL layout, per-event power-fail atomicity, sanitize behavior, later revisions, and broader ATA/SCSI diagnostic genealogy.\n')
    roadmap_text = roadmap_text.replace(phase, phase + item, 1)
ROADMAP.write_text(roadmap_text.rstrip() + '\n', encoding='utf-8')

# Normalize touched files and assert integration markers.
for path in (CASE, EVIDENCE, ROADMAP, INDEX):
    text = path.read_text(encoding='utf-8')
    cleaned = '\n'.join(line.rstrip() for line in text.splitlines()).rstrip() + '\n'
    path.write_text(cleaned, encoding='utf-8')

assert CASE_MARKER in CASE.read_text(encoding='utf-8')
assert EVIDENCE_MARKER in EVIDENCE.read_text(encoding='utf-8')
assert ROADMAP_MARKER in ROADMAP.read_text(encoding='utf-8')
assert INDEX_MARKER in INDEX.read_text(encoding='utf-8')
assert 'expanded 2011–2021 NVMe log-lifetime/PEL/retrieval-validity grounding' in INDEX.read_text(encoding='utf-8')
print('Case 66 PEL retrieval-validity deepening integrated')
