from pathlib import Path

EVIDENCE_PATH = Path('evidence/110-netapp-2003-2026-snaplock-onprem-worm-deepening.md')
EVIDENCE = r'''# Evidence 110 deepening — NetApp SnapLock on-premises disk WORM, 2003 prior-art and retention-clock boundary

## Case

[`cases/110-amazon-s3-object-lock-version-worm-retention.md`](../cases/110-amazon-s3-object-lock-version-worm-retention.md)

## Evidence status

**Grounded for a bounded on-premises WORM prior-art and retention-control comparison.**

This pass adds **NetApp SnapLock** as a named pre-cloud WORM system. It is deliberately narrower than a history of compliant storage: the goal is to establish that software/controller-enforced WORM on ordinary disk-based network storage was publicly documented by 2003, then compare its retained file/clock/authority relations with the later cloud-object contracts already grounded in Case 110.

It does **not** claim that NetApp invented disk WORM, that SnapLock is the direct ancestor of S3 Object Lock, or that the current ONTAP implementation is unchanged from 2003.

Claim labels follow [`docs/METHOD.md`](../docs/METHOD.md):

- **H** — historical record;
- **P** — primary/provider evidence;
- **P\*** — provider documentation preserved on a non-origin mirror;
- **E** — engineering reconstruction from documented behavior;
- **A** — functional analogy/comparison;
- **I** — bounded philosophical interpretation;
- **X** — explicit exclusion / unsupported stronger claim.

## Sources

### P1 — Network Appliance FY2003 Form 10-K

Network Appliance, Inc., **Form 10-K for the fiscal year ended 25 April 2003**, filed with the U.S. Securities and Exchange Commission.

<https://www.sec.gov/Archives/edgar/data/1002047/000089161803003272/f91038e10vk.htm>

The filing says **SnapLock was introduced during fiscal year 2003** and describes it as meeting regulatory `data permanence` requirements by providing WORM attributes, including nonerasability and nonrewritability, for data stored on NearStore. The same filing describes NearStore as disk-based nearline storage.

Evidence strength: **strong period, company-authored public filing**.

Chronology limit: this establishes introduction no later than the fiscal year ending 25 April 2003. It does not by itself establish an exact public-launch day or invention priority.

### P2 — Network Appliance FY2004 Q2 Form 10-Q

Network Appliance, Inc., **Form 10-Q for the quarter / six months ended 31 October 2003**.

<https://www.sec.gov/Archives/edgar/data/1002047/000089161803006173/f94954e10vq.htm>

The filing says SnapLock Compliance and SnapLock Enterprise were then available on NetApp FAS servers **in addition to the NearStore platform**, and distinguishes the regulated-data purpose of Compliance from the broader data-integrity/governance purpose of Enterprise.

Evidence strength: **strong period, company-authored public filing**.

This later-2003 record is used to establish product/mode availability, not to rewrite the exact feature set of the earlier fiscal-2003 introduction.

### P*3 — Data ONTAP 7-era NetApp documentation preserved by University of Wollongong

NetApp documentation mirror, **“What SnapLock is”** and **“What the ComplianceClock is.”**

<https://documents.uow.edu.au/~blane/netapp/ontap/archive/complying/concept/c_oc_cmpl_snplk-what-is.html>

<https://documents.uow.edu.au/~blane/netapp/ontap/archive/complying/concept/c_oc_cmpl_snplk-comlplianceclock-what-is.html>

The preserved vendor documentation describes SnapLock as a **license-based, disk-based, open-protocol** feature that provides storage-enforced WORM and retention over CIFS/NFS at individual-file granularity. It also states that SnapLock is a persistent property of SnapLock volumes/files and remains enforced regardless of licensing state. The companion ComplianceClock page describes a secure software time base, replicated/retained in system/volume-related state, used so ordinary system-clock changes cannot prematurely release compliant data.

Evidence strength: **useful provider-text historical witness, but not origin-hosted**. The mirror appears to preserve Data ONTAP 7-generation documentation. It is therefore not used as proof that every listed detail existed in the April-2003 release.

### P4 — current ONTAP SnapLock overview, 16 June 2026

NetApp, **“Learn about ONTAP SnapLock,”** updated 16 June 2026.

<https://docs.netapp.com/us-en/ontap/snaplock/>

Current documentation states that SnapLock creates special-purpose volumes in which files can be committed to non-erasable, non-writable WORM state for a defined period or indefinitely, at file level over NFS/CIFS. It distinguishes **Compliance** and **Enterprise** modes: current Compliance does not permit deletion of retained WORM files, while current Enterprise permits an audited privileged-delete path. It also states that, after retention expires, the operator remains responsible for deleting files no longer required, and that a file committed to WORM cannot be modified even after expiry.

Evidence strength: **strong current provider contract**, not a frozen 2003 witness.

### P5 — current retention-time contract, 16 June 2026

NetApp, **“Set the ONTAP SnapLock retention time,”** updated 16 June 2026.

<https://docs.netapp.com/us-en/ontap/snaplock/set-retention-period-task.html>

Current documentation distinguishes a **retention period** (duration after WORM commit) from a **retention time** (the absolute time after which the file no longer needs to be retained). It states that after a file is committed to WORM the retention period/time may be extended but not shortened, and that an explicitly set file retention time is stored in the file's `atime` field.

Evidence strength: **strong current provider contract**.

### P6 — current Compliance Clock contract, 16 April 2026

NetApp, **“Initialize the ONTAP Compliance Clock,”** updated 16 April 2026.

<https://docs.netapp.com/us-en/ontap/snaplock/initialize-complianceclock-task.html>

Current documentation states that the volume Compliance Clock controls WORM-file retention periods and inherits its initial time from a system Compliance Clock. It also records an important version boundary: in ONTAP 9.13.1 and earlier the node clock could not be reinitialized after initialization; beginning with ONTAP 9.14.1 reinitialization is allowed only under restrictive conditions, including the absence of SnapLock volumes and locked-snapshot state.

Evidence strength: **strong current provider contract and explicit version boundary**.

## Historical record

### H/P — a named disk-based WORM system was public by fiscal 2003

P1 is a contemporary corporate filing, not a later retrospective. It says SnapLock was introduced during fiscal year 2003 and supplied WORM nonerasability/nonrewritability for data on NearStore. Because that fiscal year ended **25 April 2003**, the safe lower bound is:

```text
NetApp SnapLock public/product history by FY ended 25 Apr 2003
    <<
Azure / GCS / S3 public cloud-WORM launches in 2018
```

This materially narrows Case 110's prior-art boundary. The cloud services did not invent the general idea of enforcing WORM semantics through a managed storage system built on rewritable disks.

The evidence does **not** establish that SnapLock was first. Other compliant-storage products, including content-addressed systems, require their own chronology if invention or market priority ever matters.

### H/P — late-2003 SnapLock already had multiple policy/authority modes

P2 records both SnapLock Compliance and SnapLock Enterprise as available on FAS as well as NearStore by the quarter ended 31 October 2003. That demonstrates that `WORM` was already a family of authority contracts in this product line rather than one undifferentiated bit-level property.

The exact later/current semantics of those two modes are not projected backward wholesale into the fiscal-2003 introduction.

### H/P* — later Data ONTAP 7 documentation explicitly called SnapLock disk-based and open-protocol

P*3 is useful because it states the architectural claim directly: SnapLock is described as disk-based and enforced through Data ONTAP while clients use ordinary CIFS/NFS file protocols. That is a closer functional prior art to cloud policy WORM than ECMA-153 optical WORM, because the carrier need not itself be a physically write-once optical medium.

The mirror's provenance is weaker than P1/P2, so it supports mechanism continuity rather than exact 2003 launch wording.

## Engineering reconstruction

### E1 — rewrite-capable substrate != rewrite-authorized retained object

The period record and later product documentation together show a WORM relation implemented on disk-based network storage. The retention property therefore cannot be reduced to `the medium is physically incapable of another write`.

For the bounded SnapLock system, at least these layers are separable:

```text
physical disk/SSD embodiment
    !=
file identity and WORM state
    !=
retention deadline
    !=
clock used to judge expiry
    !=
authority allowed to delete
```

This is the on-premises counterpart to Case 110's existing rule `service-level WORM != physically write-once medium`.

### E2 — file-level WORM != object-version WORM

SnapLock's documented protected identity is a file in a SnapLock volume, exposed through file protocols. S3 Object Lock protects a specific S3 object version; GCS 2018 Bucket Lock applied a bucket policy; Azure's 2018 witness was container-scoped.

Thus a shared `WORM` category does not define one universal retained object:

```text
same WORM vocabulary
    !=
same identity granularity
    !=
same currentness/version relation
```

### E3 — a retention deadline needs an admissible reference clock

P*3/P6 expose the time source as explicit retained control infrastructure. A file's deadline is not self-executing: deletion admission depends on comparing retained retention state against a clock that the storage system treats as authoritative.

Therefore:

```text
retention timestamp exists
    !=
ordinary wall/system clock may redefine expiry at will
```

The engineering point is not that ComplianceClock is unique. It is that time-based retention contains a hidden **time-authority relation** in addition to the payload and deadline value.

### E4 — retention time stored in `atime` != access-history retention

P5 says current ONTAP stores an explicitly set retention time in the file's `atime` field. That means the same conventional metadata slot can carry a SnapLock-specific future-admission meaning.

This supports a narrow distinction:

```text
field name / conventional metadata role
    !=
semantic role under a retention regime
```

It does not imply that current ONTAP preserves a complete access history; in this path, `atime` is evidence about a future retention boundary.

### E5 — retention expiry != deletion, and expiry != restored mutability

P4 says that after retention expires the operator is responsible for deleting files no longer needed. It separately says a file committed to WORM cannot be modified even after the retention period has expired.

Thus current SnapLock gives a particularly useful decomposition:

```text
retention obligation satisfied
    !=
file deleted
    !=
ordinary in-place mutability restored
    !=
physical sanitization
```

This is not identical to the lifecycle/currentness behavior of S3, GCS, or Azure.

### E6 — protection lifetime can outlive licensing/capability-admission state

P*3 says existing SnapLock volume/file WORM properties remain enforced even if the SnapLock license is removed; licensing is needed for creating new protected volumes/commits rather than for dissolving already established protection.

So, for that documented Data ONTAP generation:

```text
ability to create new WORM state
    !=
continued enforcement of existing WORM state
```

A capability-control relation and an already-committed retention relation can have different lifetimes.

### E7 — retention-rule mutability != retention duration

P5 says a committed file's retention period/time can be extended but not shortened. The retained rule therefore has both a value and an authority relation governing which direction that value may move.

This is functionally comparable to locked cloud retention policies but does not imply identical implementation or legal semantics.

## Cross-provider comparison

| Relation | NetApp SnapLock | Azure/GCS/S3 Case-110 cloud evidence |
| --- | --- | --- |
| dated public floor used here | FY ended 25-Apr-2003 | 2018 provider launches |
| carrier/service class | on-premises managed disk storage | hyperscale cloud object/blob storage |
| protected identity established here | file in SnapLock volume | container/bucket/object-version depending provider/date |
| WORM enforced by managed control state | yes | yes at service-contract layer |
| physical write-once carrier required by evidence | no | no |
| explicit retained time-authority apparatus exposed | ComplianceClock | provider clocks are implicit; retain-until/policy state is exposed |
| expiry itself deletes payload | no | no in the bounded contracts |
| authority modes have identical semantics | no | no |

### A — `Compliance` and `Enterprise/Governance` labels are false friends unless mechanism is checked

NetApp and AWS both use `Compliance`, while NetApp's looser mode is called `Enterprise` and S3's is `Governance`. Similar mode names/functions are useful comparison prompts, not a translation table.

Current NetApp Enterprise uses an audited privileged-delete path; S3 Governance uses its own permission plus explicit bypass contract. Their scope, identity, clock, request, and audit semantics are separately defined.

Therefore:

```text
SnapLock Compliance != S3 Compliance by name alone
SnapLock Enterprise != S3 Governance by function alone
```

No implementation genealogy is inferred.

### A — on-premises WORM prior art != cloud-WORM genealogy

The safe historical conclusion is only chronological and functional:

> managed storage could impose WORM retention on rewritable disk-based storage at least by NetApp's fiscal 2003 SnapLock product generation, long before the 2018 cloud services in Case 110.

That does not show that Azure, Google, or AWS copied SnapLock, inherited its data structures, or adopted its ComplianceClock design.

## Philosophical interpretation — bounded

### I — time-based retention retains a rule about future admissibility, not only a payload

The technical fact is concrete: current SnapLock keeps a file WORM state, retention time, and an authoritative Compliance Clock relation that together determine when deletion can become admissible.

A narrow interpretation is:

> a technically retained object can include a retained constraint on **when a future operation is allowed to count as legitimate**, and that constraint itself depends on maintained control state.

The limit is equally important. ComplianceClock is not `time itself`, policy is not a physical force, and this file-level control state is not automatically Stieglerian tertiary retention or Heideggerian `Bestand`.

## Anti-anachronism and negative claims

This deepening does **not** establish:

- an exact calendar-day SnapLock launch before 25 April 2003;
- that SnapLock was the first disk-based or software-enforced WORM product;
- a NetApp -> Azure/GCS/AWS genealogy;
- that current ONTAP SnapLock semantics were all present in the initial fiscal-2003 product;
- that Data ONTAP 7-era mirrored documentation is an origin-hosted facsimile;
- that current `Compliance` / `Enterprise` semantics exactly equal the 2003 modes;
- that `atime` is a universal retention-metadata field outside current SnapLock;
- that ComplianceClock has had one unchanged initialization/synchronization contract across releases;
- that `disk-level` protection in current NetApp vocabulary means the magnetic/Flash medium is physically write-once;
- that expiry, privileged deletion, file unlink, block reclamation, key retirement, or media sanitization are one event;
- regulatory or legal sufficiency for any particular deployment.

P6 explicitly blocks one especially easy backward projection: ONTAP 9.14.1 changed ComplianceClock reinitialization possibilities under restricted no-protected-state conditions. Current clock-management semantics therefore must be versioned rather than treated as timeless SnapLock essence.

## Related-repository boundary

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated `SnapLock` case to reuse. If broader compliant-storage history is developed — EMC Centera, optical-to-disk WORM migration, WAFL/ONTAP implementation, regulation-driven product design, or exact release genealogy — it belongs primarily there.

`technical-retention` keeps only the bounded relation needed here:

> **rewritable disk embodiment + retained WORM state + retention deadline + authoritative clock + deletion authority can make a file operationally non-rewritable/non-erasable without turning the underlying medium into a physically write-once carrier.**

## Readiness

This on-premises prior-art slice is complete enough to integrate into grounded Case 110 because it has:

- a period first-party SEC filing establishing SnapLock introduction and WORM purpose by fiscal 2003;
- an independent later-2003 first-party filing establishing Compliance/Enterprise product availability;
- preserved vendor documentation exposing the disk/open-protocol/file/ComplianceClock mechanism, with mirror provenance labeled rather than hidden;
- current first-party documentation exposing present retention-time, expiry, mode, and clock semantics with explicit version boundaries;
- negative claims preventing priority, genealogy, physical-WORM, sanitization, and current-to-2003 back-projection.

Remaining work should be separate slices: exact 2003 product-release/ONTAP revision archaeology, EMC Centera and other disk-WORM chronology, regulation/certification history, internal WAFL retention implementation, lower-layer deletion/sanitization, and fault/clock-manipulation validation.
'''

CASE_SECTION = r'''
## NetApp SnapLock on-premises WORM deepening

### H/P — fiscal-2003 SnapLock supplies a much earlier managed disk-WORM floor

Network Appliance's Form 10-K for the fiscal year ended **25 April 2003** says SnapLock was introduced during fiscal 2003 and provided WORM nonerasability/nonrewritability for data stored on NearStore. A later 2003 Form 10-Q records SnapLock Compliance and SnapLock Enterprise on FAS systems in addition to NearStore. This moves the nearest named non-optical prior-art floor for this case back roughly fifteen years before the 2018 cloud-service comparison.

The conclusion is deliberately narrow:

```text
2018 cloud Object/Blob WORM
    !=
invention of managed WORM semantics on rewritable disk storage
```

It does **not** establish that SnapLock was the first disk WORM product or that Azure, Google, or AWS descended from it.

### H/P* / E — disk-based file WORM separates carrier mutability from operation authority

Data ONTAP 7-generation NetApp documentation preserved on a University of Wollongong mirror explicitly calls SnapLock a **disk-based, open-protocol** feature providing storage-enforced WORM through CIFS/NFS at individual-file granularity. Current ONTAP documentation independently preserves the file-level WORM model.

That gives a closer functional counterexample than optical WORM:

```text
physical carrier can be rewrite-capable
    while
retained file/control state refuses rewrite/delete operations
```

`service/storage-enforced WORM` is therefore not evidence of physically write-once disk or Flash cells.

### H/P* / P-current — retention depends on retained time authority as well as a deadline

The historical Data ONTAP 7 documentation exposes **ComplianceClock** as a protected time base, while current ONTAP documentation separates system and volume Compliance Clocks and says the volume clock controls file-retention decisions. Current documentation also says an explicit retention time is stored in the file's `atime` and can be extended but not shortened after WORM commit.

This permits a bounded decomposition:

```text
file payload
    !=
WORM state
    !=
retention deadline
    !=
authoritative clock for evaluating that deadline
    !=
deletion authority
```

The `atime` usage is a current SnapLock contract, not proof that every historical or non-NetApp WORM system uses access-time metadata this way.

### P-current / E — expiry changes deletion admission without restoring ordinary mutability

Current NetApp documentation says expired WORM files are not automatically deleted: operators must delete those no longer required. It also says a file committed to WORM cannot be modified even after the retention period expires.

Thus SnapLock sharpens a relation already present in the cloud cases:

```text
retention expiry
    !=
automatic deletion
    !=
ordinary write mutability restored
    !=
physical sanitization
```

### H/P* / E — licensing lifetime can differ from existing-protection lifetime

The preserved Data ONTAP documentation states that already established SnapLock volume/file WORM properties remain enforced regardless of licensing state; the license controls creation of new SnapLock volumes/commits rather than dissolving prior protection. For that documented generation, `ability to create new protected state != lifetime of already-committed protection`.

### A / X — similar mode names do not create a provider-independent state machine

NetApp and AWS both use `Compliance` vocabulary, but current SnapLock Compliance/Enterprise and S3 Compliance/Governance have separately defined scopes and bypass paths. NetApp Enterprise privileged delete is not silently renamed S3 Governance bypass, and SnapLock Compliance is not assumed to share S3's object-version model.

The comparison is functional only. No SnapLock -> S3/Azure/GCS genealogy is claimed.

### Anti-anachronism boundary

Current ONTAP documentation explicitly records a ComplianceClock-management change beginning with **ONTAP 9.14.1**, permitting reinitialization only when protected SnapLock/locking state is absent and other conditions hold. That is enough to reject an invariant `SnapLock clock semantics never changed` story. The fiscal-2003 launch, Data ONTAP 7-generation mirror, and current ONTAP contract remain three distinct evidence layers.

Full source mapping and limits are in [`evidence/110-netapp-2003-2026-snaplock-onprem-worm-deepening.md`](../evidence/110-netapp-2003-2026-snaplock-onprem-worm-deepening.md).
'''

ROADMAP_LINE = "- [x] Case 110 NetApp SnapLock fiscal-2003 on-premises disk-WORM / retention-clock prior-art deepening — [`evidence/110-netapp-2003-2026-snaplock-onprem-worm-deepening.md`](evidence/110-netapp-2003-2026-snaplock-onprem-worm-deepening.md): Network Appliance's FY2003 SEC filing supplies a named managed disk-WORM floor roughly fifteen years before the 2018 cloud services, while later Data ONTAP vendor documentation and current ONTAP docs separate file-level WORM state, retention deadline, ComplianceClock time authority, licensing/capability admission, expiry, deletion, and physical sanitization. This closes the bounded `rewritable carrier != rewrite authority`, `deadline != authoritative clock`, `expiry != deletion/mutability restoration`, and `same Compliance vocabulary != same provider state machine` seams without claiming SnapLock invention priority or a NetApp→cloud genealogy. Exact 2003 release/ONTAP genealogy, EMC Centera/other disk-WORM chronology, WAFL internals, certification history, lower-layer sanitization, and fault/clock validation remain open."

INDEX_APPEND = r'''
## Case 110 deepening — NetApp SnapLock on-premises disk-WORM findings

Deepening record: [`evidence/110-netapp-2003-2026-snaplock-onprem-worm-deepening.md`](evidence/110-netapp-2003-2026-snaplock-onprem-worm-deepening.md).

- **3083 — fiscal-2003 introduction floor != exact launch day:** Network Appliance's 10-K says SnapLock was introduced during the fiscal year ended 25 April 2003; it does not supply a precise public-release date. (`H/P`, `X`)
- **3084 — managed disk WORM predates 2018 cloud WORM:** the period filing puts WORM nonerasability/nonrewritability on NearStore roughly fifteen years before the Azure/GCS/S3 service launches already grounded in Case 110. (`H/P`)
- **3085 — earlier SnapLock chronology != disk-WORM invention priority or cloud genealogy:** the dated floor blocks a cloud-origin shortcut without proving first invention, market priority, copying, or causal descent. (`H/P`, `X`)
- **3086 — rewritable disk embodiment != rewrite-authorized retained object:** Data ONTAP-era documentation explicitly describes SnapLock as disk-based while enforcing non-rewritable file state through the storage system. (`H/P*`, `E`)
- **3087 — file-level WORM != S3 object-version WORM != 2018 bucket/container WORM:** shared category language does not normalize the protected identity or currentness relation. (`H/P*`, `A`, `X`)
- **3088 — WORM state != payload:** the retained prohibition/commit state that controls later operations is a relation about a file, not another copy of the file's user bytes. (`E`)
- **3089 — retention deadline != authoritative retention clock:** ComplianceClock is separately retained/maintained control state used to decide whether time-based protection has expired. (`H/P*`, `P`, `E`)
- **3090 — current SnapLock `atime` retention semantics != access-history retention:** current ONTAP stores explicit retention time in the file's `atime`; that field carries a future-admission boundary here, not a complete history of prior accesses. (`H/P`, `E`, `X`)
- **3091 — retention expiry != automatic deletion:** current NetApp says operators remain responsible for deleting WORM files after their retention period. (`H/P`, `E`)
- **3092 — retention expiry != ordinary in-place mutability restored:** current SnapLock says a committed WORM file remains non-modifiable even after the retention period expires. (`H/P`, `E`)
- **3093 — post-commit extension authority != shortening authority:** current retention time/period may be extended but not shortened after WORM commit. (`H/P`, `E`)
- **3094 — license/capability state != already-established protection state:** preserved Data ONTAP documentation says existing SnapLock volume/file WORM properties remain enforced regardless of licensing state. (`H/P*`, `E`)
- **3095 — ability to create new WORM state != lifetime of existing WORM state:** for the documented Data ONTAP generation, removal of creation capability does not dissolve already committed protection. (`H/P*`, `E`)
- **3096 — SnapLock Compliance/Enterprise != S3 Compliance/Governance:** similar names and stronger/weaker policy roles do not establish identical bypass authority, object scope, request semantics, audit behavior, or genealogy. (`A`, `X`)
- **3097 — current NetApp `disk-level` Compliance protection != physically write-once medium:** current ONTAP also supports SSDs and describes an integrated hardware/software solution; product protection-level vocabulary is not proof of immutable cells. (`H/P`, `E`, `X`)
- **3098 — ComplianceClock semantics must be versioned:** current NetApp explicitly distinguishes ONTAP 9.13.1-and-earlier initialization behavior from the restricted reinitialization path beginning in 9.14.1. (`H/P`, `X`)
- **3099 — WORM expiry/deletion != media sanitization:** allowing/deleting an expired file does not establish block overwrite, Flash erase, key destruction, or forensic disappearance. (`E`, `X`)
- **3100 — related-repository boundary:** a fresh `tmzncty/computing-archaeology` search found no dedicated SnapLock study; broad compliant-storage/WAFL/EMC-Centera/release genealogy belongs there if developed, while this deepening stays with retention-policy, time-authority, and prior-art relations. (`H/P` project-state record)
'''

if EVIDENCE_PATH.exists():
    raise SystemExit(f'{EVIDENCE_PATH} already exists')
EVIDENCE_PATH.write_text(EVIDENCE.rstrip() + '\n', encoding='utf-8')

case_path = Path('cases/110-amazon-s3-object-lock-version-worm-retention.md')
case = case_path.read_text(encoding='utf-8')
if EVIDENCE_PATH.name not in case:
    marker = '\n## Engineering reconstruction\n'
    if marker not in case:
        raise SystemExit('Case 110 engineering marker not found')
    case = case.replace(marker, '\n' + CASE_SECTION.strip() + '\n\n## Engineering reconstruction\n', 1)
    case_path.write_text(case, encoding='utf-8')

roadmap_path = Path('ROADMAP.md')
roadmap = roadmap_path.read_text(encoding='utf-8')
if EVIDENCE_PATH.name not in roadmap:
    lines = roadmap.splitlines()
    insert_at = None
    for i, line in enumerate(lines):
        if 'Case 110 Google Cloud Storage 2018 Bucket Lock prior-art / policy-scope deepening' in line:
            insert_at = i + 1
            break
    if insert_at is None:
        raise SystemExit('ROADMAP Case 110 GCS marker not found')
    lines.insert(insert_at, ROADMAP_LINE)
    roadmap = '\n'.join(lines) + ('\n' if roadmap.endswith('\n') else '')
    roadmap_path.write_text(roadmap, encoding='utf-8')

index_path = Path('CASE_INDEX.md')
index = index_path.read_text(encoding='utf-8')
if EVIDENCE_PATH.name not in index:
    if '- **3082 —' not in index:
        raise SystemExit('CASE_INDEX expected 3082 predecessor not found')
    if '- **3083 —' in index:
        raise SystemExit('CASE_INDEX 3083 already occupied')
    index = index.rstrip() + '\n\n' + INDEX_APPEND.strip() + '\n'
    index_path.write_text(index, encoding='utf-8')

# Final integration tree must not retain automation scaffolding.
Path('_automation_case110_snaplock.py').unlink(missing_ok=True)
Path('.github/workflows/tmp-case110-snaplock.yml').unlink(missing_ok=True)
