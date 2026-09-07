from pathlib import Path

CASE_PATH = Path('cases/110-amazon-s3-object-lock-version-worm-retention.md')
EVIDENCE_PATH = Path('evidence/110-amazon-s3-2018-object-lock-grounding.md')
ROADMAP = Path('ROADMAP.md')
INDEX = Path('CASE_INDEX.md')
CASE109 = Path('cases/109-amazon-s3-versioning-delete-marker-lifecycle.md')

case_text = r'''# Amazon S3 Object Lock: Per-Version WORM Retention, Legal Holds, and Delete-Marker Boundaries

## Status

**`grounded`** for the bounded public service-contract relation described below.

## Scope

- **Object / system:** Amazon S3 general-purpose buckets using S3 Versioning and S3 Object Lock.
- **Historical anchor:** AWS's public announcement of S3 Object Lock on **26 November 2018**.
- **Later contract evidence:** current AWS User Guide documentation is used to clarify the presently documented semantics of per-version retention, Governance/Compliance modes, legal holds, simple versus version-specific deletion, and Lifecycle interaction. Those current details are not silently projected backward as exact 2018 wording.
- **Prior-art floor:** ECMA-153's June 1994 second edition standardizes a magneto-optical Write Once, Read Multiple (WORM) cartridge. It is used only to block an S3-first/WORM-invention claim, not to assert a direct engineering genealogy.
- **Research question:** what exactly is retained when an object version is WORM-protected by service policy, and how can key currentness, delete markers, lifecycle policy, legal hold, and retention expiry change without being the same operation as deletion or physical erasure?

This is **not** a history of S3 internals, physical media immutability, replica placement, encryption-key destruction, compliance law, cross-region replication, or the invention history of WORM media. It is a bounded continuation of Case 109's distinction between version history and immutable retention.

The bounded retention claim is:

> **S3 Object Lock protects a specified object version through retained service-level control state. That protection does not freeze the logical key as a whole: later versions or a delete marker may become current while the protected predecessor remains locked. Governance retention, Compliance retention, and legal hold are distinct authorization/time relations; expiry or hold removal ends one deletion barrier but does not itself delete the version, reclaim its physical embodiment, or prove sanitization.**

`protection barrier`, `currentness`, `retention authority`, and `service-level WORM` are project engineering terms unless explicitly attributed to AWS.

## Historical vocabulary

AWS sources use:

- `S3 Object Lock` / `Object Lock`;
- `write-once-read-many (WORM)`;
- `object version`;
- `retention period`;
- `Retain Until Date`;
- `Compliance mode`;
- `Governance mode`;
- `legal hold`;
- `BypassGovernanceRetention`;
- `delete marker`;
- `Versioning`;
- `Lifecycle`.

The following are project terms, not AWS historical vocabulary:

- `protection barrier`;
- `service-level WORM`;
- `retention-control state`;
- `key currentness layer`;
- `physical-embodiment immutability`.

## Historical record

### H/P — 26 November 2018: S3 Object Lock is publicly announced

AWS announced **Amazon S3 Object Lock** on 26 November 2018 as a new S3 feature that blocks deletion of object versions during a customer-defined retention period. AWS explicitly presented it as a way to migrate workloads from existing WORM systems and said protection persists through S3 storage-class lifecycle transitions.

The announcement is a strong public service-availability floor. It is not evidence that AWS invented WORM retention, object immutability, legal holds, or the underlying storage mechanisms.

Primary anchor: AWS, **“AWS Announces Amazon S3 Object Lock in all AWS Regions,”** 26 November 2018.

### H/P — Object Lock is version-scoped rather than key-freezing

Current AWS documentation states that Object Lock works with S3 Versioning and that a retention period or legal hold protects **only the object version specified**. It explicitly says protection does not prevent a new version from being created or a delete marker from being placed on top of the protected version.

Therefore:

```text
protected object version
    ≠
logical key frozen against all later current versions
```

A new PUT can create another version with the same key while the older protected version keeps its own retention configuration.

### H/P — retention time is retained metadata attached to a version

AWS states that when a retention period is placed on an object version, S3 stores a timestamp in that version's metadata indicating when the retention period expires. Different versions of one object can carry different retention modes and periods.

This directly exposes retained **control state about future admissibility** in addition to the payload itself.

The `Retain Until Date` is not a physical lifetime prediction for the medium. It is a service-policy boundary for overwrite/delete protection.

### H/P — expiry ends a retention barrier, not the object by itself

Current AWS documentation says that after the retention period expires, the object version **can be** overwritten or deleted. The grammar matters: expiry changes what operations are authorized; it is not itself described as a DELETE, reclamation event, or physical erase.

Thus:

```text
retention-period expiry
    ≠
automatic version deletion
    ≠
physical sanitization
```

A separate delete or lifecycle action is still needed to retire the version at the service layer, subject to any remaining legal hold.

### H/P — Compliance and Governance are different authority relations

Current AWS documentation distinguishes two retention modes.

In **Compliance mode**, a protected object version cannot be overwritten or deleted by any user, including the account root user, and its retention mode cannot be changed or its period shortened before expiry.

In **Governance mode**, protection can be overridden by a principal with `s3:BypassGovernanceRetention`, and the request must explicitly invoke the governance bypass path.

So `WORM-protected` is not one undifferentiated authorization state. The mode changes who, if anyone, can deliberately cross the protection barrier before the ordinary retain-until time.

### H/P — legal hold is independent of the fixed retention clock

AWS documents legal hold as version-scoped protection with **no expiration date**. It remains until explicitly removed by an authorized principal and is independent of retention periods.

A version can therefore carry both relations at once:

```text
fixed retention period
+
indefinite-until-removed legal hold
```

Expiration of the time-based retention period does not make the object deletable while a legal hold still applies; removing the legal hold does not make it deletable while an unexpired retention period still applies.

### H/P — simple DELETE can change currentness without deleting the protected version

AWS documents two deletion paths for a protected version:

- a permanent/version-specific DELETE of the protected version is denied while its active retention/hold barrier applies;
- a simple DELETE without a version ID can still succeed by inserting a **delete marker**, which becomes the current version.

Object Lock considerations additionally state that delete markers are not WORM-protected by the retention period or legal hold on the underlying object version.

This gives a particularly sharp boundary:

```text
current key view becomes a delete marker
    ≠
protected predecessor was deleted
```

Case 109's default-view/current-version distinction therefore survives even when a predecessor is WORM-protected.

### H/P — Lifecycle can advance while a locked version remains undeletable

AWS's Object Lock considerations say Lifecycle configurations continue to function on protected objects, including creation of delete markers and storage-class transitions, but a locked object version cannot be deleted by a Lifecycle expiration policy while the lock remains active.

Hence:

```text
lifecycle policy continues
    ≠
active Object Lock barrier has been overridden
```

The retention relation and the lifecycle relation compose rather than collapse into one timer.

## Engineering reconstruction

### E — retained state decomposition

The public service contract requires at least these distinct retained relations:

1. **logical key** — the ordinary object name;
2. **version identity** — the particular historical object version;
3. **payload** — the data represented by that version;
4. **current/noncurrent relation** — which version or marker ordinary key access sees;
5. **retention mode** — Governance or Compliance for a protected version;
6. **retain-until timestamp** — a time boundary stored in version metadata;
7. **legal-hold status** — a separate version-scoped protection relation without a fixed expiry;
8. **authorization state** — permissions relevant to setting/removing holds or bypassing Governance;
9. **lifecycle policy** — a separate policy that may transition objects, create markers, or later delete versions when allowed.

This decomposition is an engineering reconstruction from the documented contract. AWS does not present it as a universal storage ontology.

### E — two different notions of “write once” must not be collapsed

For this bounded case, `WORM` is a **service-level admissibility guarantee** over an object version: the API will refuse certain overwrite/delete operations while specified protection holds.

That is different from saying the underlying medium is physically incapable of changing.

The public Object Lock sources do not establish:

- which SSD/HDD/tape cells carry the object;
- whether physical replicas are rewritten or migrated;
- whether encryption keys change;
- how many lower-level embodiments exist;
- whether a backend garbage collector moves protected data;
- what sanitization process occurs after service-level deletion.

Therefore:

```text
service-level WORM
    ≠
physically write-once medium
```

## Prior art and historical boundary

### H/P — WORM media clearly predates the 2018 S3 feature

ECMA-153, second edition **June 1994**, is titled **“Information interchange on 130 mm optical disk cartridges of the Write Once, Read Multiple (WORM) type, using the magneto-optical effect.”** Its official summary specifies recording information once and reading it many times.

This is enough to establish:

```text
S3 Object Lock launch in 2018
    ≠
invention of WORM as a storage concept or medium regime
```

### A — the ECMA optical comparison is functional, not genealogical

The comparison is useful precisely because the mechanisms differ.

- ECMA-153 constrains a **physical optical recording medium** and interchange format.
- S3 Object Lock constrains **service operations on a named object version** through retained policy/authorization state.

The sources inspected here do not establish that S3 Object Lock descends technically from ECMA-153, from that cartridge family, or from any particular optical-WORM implementation.

Earlier WORM standard ≠ demonstrated S3 genealogy.

## Cross-case comparison

### Case 109 — Versioning and delete markers

Case 109 established:

```text
current key view
    ≠
only retained version
```

Case 110 adds:

```text
retained version
    ≠
immutably protected version
```

and then:

```text
immutably protected version
    ≠
key frozen against new versions or delete markers
```

This is a layer decomposition, not a claim that Versioning and Object Lock are separate physical systems.

### ZFS snapshots / Swift tombstones / distributed-retention analogies

Other cases in this repository also separate current visibility, historical reachability, and reclamation. Those comparisons remain **functional only**. S3 Object Lock's Governance/Compliance/legal-hold contracts are not inferred for ZFS, Swift, or other systems, and their internal mechanisms are not inferred for S3.

## Failure and forgetting boundaries

For the bounded public contract, distinguish:

- **retention expiry** — time-based Object Lock protection ends;
- **Governance bypass** — an authorized exceptional path can cross Governance protection;
- **legal-hold removal** — a separate hold barrier ends;
- **delete-marker insertion** — current key visibility becomes negative while an older version may remain;
- **version-specific delete** — a selected version is removed from the S3 version service when permitted;
- **Lifecycle deletion** — policy-driven service retirement when not blocked by active Object Lock;
- **physical erasure/sanitization** — not established by the public Object Lock contract.

None of these should be substituted for another merely because all can participate in eventual forgetting.

## What this case does not establish

This bounded case does **not** establish:

- S3's internal replica/erasure-coding topology;
- the physical medium used for a locked object version;
- whether backend embodiments move while a lock is active;
- precise physical-remnant lifetime after version deletion;
- cryptographic-erasure behavior;
- full 2018→2026 Object Lock feature chronology;
- historical changes to enabling Object Lock on pre-existing buckets;
- regulatory/legal sufficiency for any particular customer;
- provider-independent equivalence with Azure, GCS, or on-premises object-lock systems;
- invention priority for WORM storage.

## Open work

- Recover a revision-sensitive Object Lock contract chronology from 2018 onward rather than projecting today's options backward.
- Compare named provider/object-store WORM contracts without flattening version scope, bypass authority, default retention, and legal holds.
- Add incident/fault evidence for governance bypass, policy misconfiguration, lifecycle interaction, or administrative recovery.
- Connect service-level version retirement to independently documented lower-layer sanitization only where evidence permits.
- Route the broader history of optical, tape, filesystem, and archival WORM mechanisms to `computing-archaeology` rather than duplicating it here.

## Sources

See [`evidence/110-amazon-s3-2018-object-lock-grounding.md`](../evidence/110-amazon-s3-2018-object-lock-grounding.md).
'''

evidence_text = r'''# Evidence 110 — Amazon S3 Object Lock, 2018 launch and current per-version WORM contract

## Case

[`cases/110-amazon-s3-object-lock-version-worm-retention.md`](../cases/110-amazon-s3-object-lock-version-worm-retention.md)

## Evidence status

**Grounded for a bounded public service-contract claim.**

The strongest historical anchor is AWS's dated **26 November 2018** S3 Object Lock announcement. Current AWS User Guide pages are used as later contract evidence for exact present-day semantics. ECMA-153 is used only as an earlier WORM prior-art floor. No source inspected here reveals S3's lower-level physical embodiment or proves a direct optical-WORM → S3 genealogy.

Claim labels follow [`docs/METHOD.md`](../docs/METHOD.md):

- **H** — historical statement;
- **P** — primary-source statement;
- **E** — engineering reconstruction from documented relations;
- **A** — functional analogy;
- **X** — explicit negative / exclusion claim.

## Source hierarchy

### P1 — AWS launch announcement, 26 November 2018

**AWS, “AWS Announces Amazon S3 Object Lock in all AWS Regions,” posted 26 November 2018.**

URL: <https://aws.amazon.com/about-aws/whats-new/2018/11/s3-object-lock/>

Directly supports:

- S3 Object Lock was publicly announced as a new S3 feature on 26 November 2018;
- it blocks object-version deletion during a customer-defined retention period;
- AWS explicitly frames it for migration from existing WORM systems;
- the launch already distinguishes Governance and Compliance modes;
- the launch states Object Lock protection survives storage-class lifecycle transitions.

Limits:

- launch wording is not silently substituted for every current User Guide detail;
- the announcement does not establish invention priority;
- it does not reveal backend physical immutability, replica layout, or media erasure.

Evidence strength: **strong historical/product-primary anchor**.

### P2 — AWS current User Guide, “Locking objects with Object Lock”

URL: <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html>

Current contract points used:

- Object Lock uses a WORM model;
- Object Lock works with S3 Versioning;
- retention periods and legal holds apply to **individual object versions**;
- protection does not prevent creation of new versions or delete markers above a protected version;
- S3 stores the retain-until timestamp in object-version metadata;
- after the retention period expires, the version becomes *eligible* for overwrite/delete rather than being automatically removed;
- Compliance mode blocks overwrite/delete even for the account root user during the retention period and does not allow shortening/changing the lock as documented;
- Governance mode can be bypassed by an appropriately authorized principal using the explicit governance-bypass path;
- legal holds have no fixed expiration and are independent of retention periods;
- a version-specific permanent DELETE can be denied while protection applies, whereas a simple DELETE can add a new current delete marker.

Evidence strength: **strong current service-contract primary documentation**.

Historical-use limit: these are current semantics. They clarify the contemporary contract and should not be cited as proof that every detail or permission name was already identical in November 2018.

### P3 — AWS current User Guide, “Object Lock considerations”

URL: <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-managing.html>

Current contract points used:

- Lifecycle configurations continue to operate on protected objects, including storage-class transitions and delete-marker behavior;
- a locked version cannot be deleted by Lifecycle expiration while its protection remains active;
- a delete marker can be created above a protected version;
- delete markers themselves are not WORM-protected merely because the underlying version has retention or legal hold.

Evidence strength: **strong current service-contract primary documentation**.

### P4 — ECMA-153, second edition, June 1994

**Ecma International, ECMA-153, “Information interchange on 130 mm optical disk cartridges of the Write Once, Read Multiple (WORM) type, using the magneto-optical effect,” 2nd edition, June 1994.**

Official HTML record: <https://ecma-international.org/publications-and-standards/standards/ecma-153/>

Directly supports:

- a formal WORM optical-disk standard exists decades before S3 Object Lock;
- the standard describes recording information once and reading it many times on a magneto-optical cartridge.

Evidence strength: **strong institutional standards-primary prior-art floor**.

Limit: this source establishes chronology and a distinct physical WORM regime. It does **not** establish a direct technical or organizational genealogy into Amazon S3 Object Lock.

## Claim-to-source map

| Claim | Type | Best source | Strength / boundary |
| --- | --- | --- | --- |
| S3 Object Lock publicly announced 26 Nov 2018 | H/P | P1 | strong dated product-primary anchor |
| launch frames Object Lock as WORM and as migration path from existing WORM systems | H/P | P1 | strong; itself argues against treating 2018 as WORM invention |
| lock protection is per object version, not a freeze on the key | P | P2 | strong current contract |
| protected predecessor may remain while a new version is created | P | P2 | strong current contract |
| retain-until time is stored in version metadata | P | P2 | strong current contract; does not expose lower-level physical metadata |
| retention expiry makes deletion/overwrite permissible rather than automatically deleting | P/E | P2 | strong text + narrow engineering inference from “can be” |
| Compliance and Governance differ in bypass authority | P | P2 | strong current contract |
| legal hold is independent and has no fixed expiry | P | P2 | strong current contract |
| simple DELETE can add a current marker above a protected predecessor | P | P2/P3 | strong current contract |
| delete marker is not WORM-protected by the predecessor's lock | P | P3 | strong current contract |
| Lifecycle cannot delete an actively locked version | P | P3 | strong current contract |
| service-level WORM does not prove physically write-once media | X/E | P1–P3 absence + API scope | strong scope exclusion; backend mechanism is undisclosed here |
| WORM predates S3 Object Lock | H/P | P4 | strong chronological floor |
| ECMA optical WORM → S3 Object Lock direct genealogy | X | P4 + no linking evidence | explicitly **not established** |

## Direct relation reconstruction

### E1 — Versioning is necessary context but not identical to Object Lock

Case 109 already grounds that Versioning can preserve predecessor versions and let a delete marker become current. P2 adds a separate retention relation on a particular version.

```text
retained historical version
    +
optional Object Lock retention/hold metadata
    =
a version that may be historically addressable and separately protected against deletion
```

This does not imply every retained version is locked.

### E2 — Object Lock protects version identity, not one immutable key state

P2 explicitly allows later versions and delete markers above a protected version. Therefore the protected relation is version-scoped.

```text
key K
  version V1 — protected until T
  version V2 — later current payload
  or marker M — later current negative state
```

The diagram is a project engineering reconstruction of the documented API relation, not AWS's internal data structure.

### E3 — time expiry and deletion are separate events

P2 says that after expiry a version can be overwritten or deleted. Therefore expiry changes the admissibility relation; it does not itself establish a deletion event.

This is the evidence basis for:

- `retention expiry ≠ automatic deletion`;
- `retention expiry ≠ physical erasure`.

### E4 — legal hold and retention period are composable barriers

P2 explicitly states they are independent and that a remaining legal hold continues protection after the fixed retention period expires, while a remaining retention period continues protection after legal-hold removal.

No extra implementation mechanism is inferred.

### E5 — current negative state can coexist with protected positive history

P2/P3 allow a simple DELETE to create a current delete marker while a protected object version remains. P3 further says the marker itself is not WORM-protected merely by the underlying version's protection.

This is a strong service-level witness that:

```text
currentness
retained predecessor
retention protection
```

are three different relations.

## Prior-art boundary

P4 is deliberately used as a **floor**, not an origin claim. A standardized magneto-optical WORM regime exists by June 1994. Its mechanism concerns recording-medium properties and interchange rules, whereas P1–P3 describe a cloud object service whose protection is attached to versioned objects and authorization/time policy.

Safe conclusion:

> **2018 S3 Object Lock is not the invention of WORM storage.**

Unsafe conclusion, rejected:

> ECMA-153 optical WORM directly caused or technically evolved into S3 Object Lock.

No source in this evidence set establishes that genealogy.

## Source-bounded negative claims

The evidence does not establish:

- physical write-once media underneath S3 Object Lock;
- backend replica count or placement;
- backend compaction/migration behavior while a version is locked;
- exact sanitization or remanence after an S3 version is eventually deleted;
- cryptographic key-retirement semantics;
- full feature-by-feature Object Lock chronology from 2018 onward;
- provider-independent WORM equivalence;
- regulatory sufficiency for any deployment;
- WORM invention priority.

## Cross-repository check

`tmzncty/computing-archaeology` was checked for a dedicated `Object Lock` treatment before opening this slice. No direct reusable case was found. The broader engineering history of WORM media, archival optical storage, tape, and compliance-oriented storage should live there if developed; this evidence file retains only the historical floor needed to keep the S3 case non-anachronistic.

## Research date

Current-contract documentation rechecked **2026-09-07**. Historical claims remain anchored to their dated sources rather than to the research date.
'''

row110 = '| [Amazon S3 Object Lock: Per-Version WORM Retention, Legal Holds, and Delete-Marker Boundaries](cases/110-amazon-s3-object-lock-version-worm-retention.md) | **grounded** | versioned payload + version-scoped Governance/Compliance retention + retain-until metadata + independent legal-hold status + delete-marker/currentness relation + Lifecycle interaction | separate version retention from immutable protection; protected version from frozen key; time expiry from deletion; Governance bypass from Compliance; legal hold from retention period; service-level WORM from physical write-once media | [2018 launch + current-contract grounding](evidence/110-amazon-s3-2018-object-lock-grounding.md); full 2018→present chronology, backend embodiment/sanitization, provider comparison, compliance-law analysis, and fault validation remain separate work |'

findings = r'''## Case 110 — Amazon S3 Object Lock findings

1697. **Versioning ≠ Object Lock** — retained predecessor versions do not by themselves establish an immutable/WORM protection policy; Object Lock adds separate version-scoped retention or legal-hold state.
1698. **Object Lock scope ≠ whole-key immutability** — current AWS documentation protects a specified object version while still permitting later versions of the same key to be created.
1699. **protected version ≠ current version** — a locked predecessor can become noncurrent while retaining its protection.
1700. **delete-marker currentness ≠ protected-version deletion** — a simple DELETE can install a current delete marker while the protected payload version remains retained.
1701. **delete marker ≠ WORM-protected payload version** — current AWS Object Lock considerations state that delete markers are not WORM-protected merely by the retention or legal hold on the underlying version.
1702. **Governance mode ≠ Compliance mode** — Governance has an explicit privileged bypass path; Compliance removes that ordinary service-level bypass during the retention period, including for the account root user under the documented contract.
1703. **retain-until timestamp ≠ physical retention lifetime** — the timestamp stored with the object version governs service authorization, not a prediction of media charge, magnetic remanence, or physical embodiment survival.
1704. **retention expiry ≠ automatic deletion** — current AWS wording makes an expired version eligible to be overwritten/deleted; expiration itself is not a DELETE event.
1705. **retention expiry ≠ physical sanitization** — ending the service barrier does not prove overwrite, Flash erase, cryptographic erase, or lower-level replica reclamation.
1706. **legal hold ≠ retention period** — legal hold has no fixed expiry and is documented as independent of the fixed time-based retention relation.
1707. **legal-hold removal ≠ version deletion** — removing one protection barrier does not remove the payload version, and another unexpired retention period may still block deletion.
1708. **Lifecycle progress ≠ Object Lock override** — lifecycle transitions and marker creation can continue while an actively locked version remains undeletable by Lifecycle expiration.
1709. **service-level WORM ≠ physically write-once medium** — S3's public Object Lock contract constrains admissible API operations on versions and does not disclose an irreversible lower-level recording substrate.
1710. **same key writable again ≠ protected predecessor overwritten** — a new version can be created at the same key while the older protected version retains its own lock state.
1711. **2018 S3 Object Lock launch ≠ WORM invention priority** — ECMA-153's June-1994 optical-disk standard already specifies a Write Once, Read Multiple storage regime.
1712. **earlier WORM standard ≠ demonstrated S3 genealogy** — the ECMA optical medium provides a chronological and functional prior-art floor, not evidence of direct implementation descent into Amazon S3 Object Lock.
'''

roadmap_line = '- [x] Amazon S3 Object Lock per-version WORM / retention-authority boundary — [`cases/110-amazon-s3-object-lock-version-worm-retention.md`](cases/110-amazon-s3-object-lock-version-worm-retention.md), grounded by [`evidence/110-amazon-s3-2018-object-lock-grounding.md`](evidence/110-amazon-s3-2018-object-lock-grounding.md): the 26-Nov-2018 AWS launch anchors the public feature, while current AWS documentation separates version-scoped retention from key currentness, Governance from Compliance bypass authority, legal hold from fixed retain-until time, simple DELETE/delete-marker insertion from protected-version deletion, and Lifecycle progress from lock override. ECMA-153 (June 1994) supplies an earlier optical-WORM floor without implying genealogy. This closes only the bounded service-contract relation; full Object Lock revision chronology, backend physical embodiment/sanitization, provider comparison, regulatory analysis, and fault validation remain open.'

continuation = r'''

## Continuation

The immutable-retention layer intentionally excluded here is now handled separately in [`Case 110 — Amazon S3 Object Lock: Per-Version WORM Retention, Legal Holds, and Delete-Marker Boundaries`](110-amazon-s3-object-lock-version-worm-retention.md). Case 109 remains the Versioning/currentness/reclamation case; Case 110 asks when one retained version is additionally protected against deletion and why that still does not freeze the key or prove physical write-once media.
'''

# Write bounded new research files.
if CASE_PATH.exists() and CASE_PATH.read_text(encoding='utf-8') != case_text:
    raise SystemExit(f'{CASE_PATH} already exists with different content')
CASE_PATH.write_text(case_text, encoding='utf-8')
if EVIDENCE_PATH.exists() and EVIDENCE_PATH.read_text(encoding='utf-8') != evidence_text:
    raise SystemExit(f'{EVIDENCE_PATH} already exists with different content')
EVIDENCE_PATH.write_text(evidence_text, encoding='utf-8')

# Update predecessor with an explicit continuation without changing its bounded conclusions.
t = CASE109.read_text(encoding='utf-8')
if 'Case 110 — Amazon S3 Object Lock' not in t:
    t = t.rstrip() + continuation + '\n'
    CASE109.write_text(t, encoding='utf-8')

# Update roadmap adjacent to Case 109 when possible; fallback to the Phase-4 logical-deletion line.
t = ROADMAP.read_text(encoding='utf-8')
if 'cases/110-amazon-s3-object-lock-version-worm-retention.md' not in t:
    lines = t.splitlines()
    insert_at = None
    for i, line in enumerate(lines):
        if 'cases/109-amazon-s3-versioning-delete-marker-lifecycle.md' in line:
            insert_at = i + 1
            break
    if insert_at is None:
        for i, line in enumerate(lines):
            if line.startswith('- [ ] logical deletion / invalidation'):
                insert_at = i + 1
                break
    if insert_at is None:
        raise SystemExit('ROADMAP insertion anchor not found')
    lines.insert(insert_at, roadmap_line)
    ROADMAP.write_text('\n'.join(lines) + '\n', encoding='utf-8')

# Update Case Index table and the previous Case 109 open-work note.
t = INDEX.read_text(encoding='utf-8')
lines = t.splitlines()
if not any('cases/110-amazon-s3-object-lock-version-worm-retention.md' in line for line in lines):
    insert_at = None
    for i, line in enumerate(lines):
        if line.startswith('| [Amazon S3 Versioning:'):
            if 'internal replication topology, Object Lock, physical deletion, and provider-independent validation remain separate' in line:
                lines[i] = line.replace(
                    'internal replication topology, Object Lock, physical deletion, and provider-independent validation remain separate',
                    'Object Lock is handled separately in Case 110; internal replication topology, physical deletion, and provider-independent validation remain separate'
                )
            insert_at = i + 1
            break
    if insert_at is None:
        raise SystemExit('CASE_INDEX Case 109 row anchor not found')
    lines.insert(insert_at, row110)
    t = '\n'.join(lines) + '\n'
else:
    t = '\n'.join(lines) + '\n'

if '## Case 110 — Amazon S3 Object Lock findings' not in t:
    if '1696. **S3 delete marker ≠ Swift tombstone implementation**' not in t:
        raise SystemExit('CASE_INDEX finding 1696 anchor not found')
    t = t.rstrip() + '\n\n' + findings.rstrip() + '\n'
INDEX.write_text(t, encoding='utf-8')

# Bounded validations.
assert CASE_PATH.exists() and EVIDENCE_PATH.exists()
assert 'service-level WORM' in CASE_PATH.read_text(encoding='utf-8')
assert 'ECMA-153' in EVIDENCE_PATH.read_text(encoding='utf-8')
assert 'cases/110-amazon-s3-object-lock-version-worm-retention.md' in ROADMAP.read_text(encoding='utf-8')
idx = INDEX.read_text(encoding='utf-8')
assert idx.count('cases/110-amazon-s3-object-lock-version-worm-retention.md') == 1
assert idx.count('## Case 110 — Amazon S3 Object Lock findings') == 1
for n in range(1697, 1713):
    assert f'{n}.' in idx
assert 'Case 110 — Amazon S3 Object Lock' in CASE109.read_text(encoding='utf-8')
print('case110 integration prepared')
