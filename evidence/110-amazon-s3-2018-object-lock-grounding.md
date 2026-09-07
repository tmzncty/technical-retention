# Evidence 110 — Amazon S3 Object Lock, 2018 launch and current per-version WORM contract

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
