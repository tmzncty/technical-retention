# Evidence 110 deepening — Azure Immutable Blob Storage, 2018 cloud-WORM prior-art floor and later version-level policy semantics

## Case

[`cases/110-amazon-s3-object-lock-version-worm-retention.md`](../cases/110-amazon-s3-object-lock-version-worm-retention.md)

## Evidence status

**Grounded for a bounded cross-provider public service-contract comparison.**

This pass adds Microsoft Azure Blob Storage as a named, near-contemporary comparison to the existing Amazon S3 Object Lock case. It has two deliberately separated historical layers:

1. **June–September 2018 Azure Immutable Blob Storage** — public preview and general availability of a container-scoped cloud WORM service before AWS's 26-November-2018 S3 Object Lock launch;
2. **later/current Azure version-level WORM** — version-scoped policy semantics that depend on Blob versioning and must not be projected backward into the September-2018 container-level contract.

The result is a stronger same-class prior-art floor for Case 110 than optical WORM alone, but it is **not** a claim that Azure invented cloud WORM, that AWS copied Azure, or that the two providers implement the same internal mechanism.

Claim labels follow [`docs/METHOD.md`](../docs/METHOD.md):

- **H** — historical record;
- **P** — primary / provider documentation;
- **E** — engineering reconstruction from the documented service relation;
- **A** — functional analogy/comparison;
- **I** — bounded philosophical interpretation;
- **X** — explicit exclusion / unsupported stronger claim.

## Sources

### P1 — Microsoft Azure public preview, 19 June 2018

Microsoft Azure Blog, **“Immutable storage for Azure Storage Blobs now in public preview,”** 19 June 2018.

<https://azure.microsoft.com/en-us/blog/azure-immutable-blob-storage-now-in-public-preview/>

Directly supports:

- a public-preview date of 19 June 2018;
- provider use of `Write-Once-Read-Many (WORM)` / `immutable` vocabulary;
- time-based retention and legal-hold policies;
- all-tier applicability;
- **Blob Container level configuration**, applying to existing and new blobs in the container;
- REST support through Blob Service API version `2017-11-09` and later and Azure Storage Resource Provider API version `2018-02-01` and later.

The page now links forward to general availability. That later editorial link is not substituted for the dated preview announcement itself.

Evidence strength: **strong dated provider-primary public-disclosure anchor**.

### P2 — Microsoft Azure general availability, 18 September 2018

Microsoft Azure Blog, **“Immutable storage for Azure Storage Blobs now generally available,”** 18 September 2018.

<https://azure.microsoft.com/en-us/blog/immutable-storage-for-azure-storage-blobs-now-generally-available/>

Directly supports:

- general availability on 18 September 2018 in all Azure public regions;
- a configurable WORM/immutable state in which blobs can be created/read but not modified/deleted under the documented policy;
- time-based retention and legal hold;
- policy independence from hot/cool/archive tier;
- container-level configuration whose policy applies to all blobs in the container, existing and new;
- provider framing of the feature as protection against modification/deletion including by account administrators;
- the same REST-version floors described in P1.

Evidence strength: **strong dated provider-primary GA anchor**.

### P3 — Azure Blob versioning general availability, August 2020

Microsoft Azure Updates, **“Azure Blob versioning is now general available,”** August 2020; record last modified 31 August 2020.

<https://azure.microsoft.com/en-us/updates/azure-blob-versioning-is-now-general-available/>

Directly supports:

- Blob versioning becoming generally available in August 2020;
- version IDs and automatic retention of previous versions as a separate Azure Blob capability.

This is used as an anti-anachronism anchor: the current version-level WORM contract cannot simply be read back into the September-2018 container-scoped launch.

Evidence strength: **strong dated provider-primary feature-chronology anchor**.

### P4 — current Microsoft Learn, version-level WORM policies

Microsoft Learn, **“Version-level WORM policies for immutable blob data.”**

<https://learn.microsoft.com/en-us/azure/storage/blobs/immutable-version-level-worm-policies>

Current contract points used:

- version-level WORM may be configured at account, container, or version scope;
- version-level policies require Blob versioning;
- overwriting a blob creates a new version while preserving the previous version;
- deleting the current version makes it a previous version retained until explicitly deleted;
- each version may have one time-based retention policy and one legal hold;
- default account/container policy can be inherited when a version transition occurs;
- later changes to a default policy do not retroactively rewrite policies already inherited by existing versions;
- a locked inherited policy can be lengthened but not shortened/deleted;
- version-level WORM support on an existing container requires migration and, once enabled, cannot be removed;
- enabling version-level WORM support is distinct from actually setting an immutability policy.

Evidence strength: **strong current provider service-contract documentation**.

Historical-use limit: this is current documentation, not evidence that these exact scopes or transitions existed in 2018.

### P5 — current Azure REST contract for blob immutability policy

Microsoft Learn, **“Set Blob Immutability Policy (REST API).”**

<https://learn.microsoft.com/en-us/rest/api/storageservices/set-blob-immutability-policy>

Directly supports:

- the blob-level operation is available as of REST version `2020-06-12`;
- snapshot/version immutability policy is allowed as of that REST version;
- `unlocked` policy mode permits changing the retain-until date;
- `locked` policy mode permits extension only;
- transition from `unlocked` to `locked` is permitted, while `locked` to `unlocked` is not;
- a blob-level policy takes precedence over account/container defaults;
- ordinary replacement-style operations such as Put Blob / Copy Blob remain allowed because they create a new version.

Evidence strength: **strong current protocol-level provider documentation with an explicit version floor**.

### P6 — AWS S3 Object Lock public launch, 26 November 2018

AWS, **“AWS Announces Amazon S3 Object Lock in all AWS Regions,”** 26 November 2018.

<https://aws.amazon.com/about-aws/whats-new/2018/11/s3-object-lock/>

Used only for the bounded chronology/comparison already established by the canonical Case-110 grounding record:

- public launch date 26 November 2018;
- per-object-version retention under S3 Versioning;
- Governance and Compliance modes;
- retain-until / legal-hold paths;
- AWS's own migration framing from existing WORM systems.

Evidence strength: **strong dated provider-primary launch anchor**.

## Historical record

### H/P — Azure publicly exposed cloud Blob WORM before the S3 Object Lock launch

P1 places Azure Immutable Blob Storage in public preview on **19 June 2018**. P2 places it in **general availability on 18 September 2018**. P6 places the public S3 Object Lock launch on **26 November 2018**.

The safe chronological conclusion is therefore:

> A named hyperscale cloud blob-storage service publicly offered a WORM/immutable retention contract before the dated public launch of S3 Object Lock.

That materially tightens Case 110's novelty boundary. ECMA-153 remains an earlier physical-media WORM floor, but Azure provides a much closer service-class counterexample to any shortcut such as `S3 Object Lock = first cloud/object WORM service`.

The stronger claims remain rejected:

- `Azure invented cloud WORM` — **not established**;
- `AWS copied Azure` — **not established**;
- `Azure Immutable Blob Storage caused S3 Object Lock` — **not established**;
- private-preview/internal-development priority at either provider — **not established**.

### H/P — the 2018 Azure contract was container-scoped

P1/P2 repeatedly describe **Blob Container level configuration**. Time-based retention and legal-hold policy applied to all blobs in the container, existing and new.

Therefore the 2018 historical witness should be described as a **container-scoped WORM policy regime**. It is not evidence that Azure already had today's per-version policy graph.

### H/P — current version-level Azure semantics are a later layer

P3 dates Blob versioning GA to August 2020. P5 gives an explicit REST floor of `2020-06-12` for setting immutability policy on a blob/snapshot/version. P4 describes the current version-level WORM model.

Together these sources justify a strict chronology guardrail:

```text
Azure 2018 container-level immutable storage
    !=
current Azure version-level WORM contract silently projected backward
```

This is a history-of-contract distinction, not a claim about when Microsoft first wrote internal code for each feature.

## Current-contract engineering reconstruction

### E1 — version identity can remain protected while the logical blob name advances

Under P4/P5, versioning turns overwrite into creation of a new version rather than in-place mutation of the protected predecessor. A protected version can therefore remain retained while the ordinary name acquires a later current version.

This is functionally comparable to S3 Object Lock's separation between protected version and current key state, but the two APIs and state machines remain provider-specific.

```text
stable protected version identity
    !=
logical name frozen against later versions
```

### E2 — current policy default != retroactive rewrite of old version protection

P4 states that an existing version's inherited policy remains unchanged when the account/container default later changes. The default is therefore a rule for future inheritance, not a continuously rewritten global truth about every retained version.

```text
current default retention policy
    !=
policy state already attached to an earlier version
```

A small current control setting and the protection state of already-created versions have different temporal scopes.

### E3 — WORM capability enablement != active object protection

P4 distinguishes enabling version-level immutability support from setting an actual policy. Existing containers may undergo an irreversible migration to support version-level WORM, but that enablement alone does not make every blob version actively retained by a time policy or legal hold.

```text
feature capability / admission state
    !=
active retention barrier on a payload version
```

This is especially useful because one control transition may itself be irreversible while the data-level retention relation remains optional/version-specific.

### E4 — locked policy state has its own one-way transition

P5 documents `unlocked -> locked` and rejects `locked -> unlocked`; once locked, the retain-until date may be extended but not shortened through that operation.

The retained state is therefore not only `payload until T`. It includes a **policy-authority state** that constrains which future policy transitions remain admissible.

```text
retention deadline
    !=
policy mutability
    !=
version currentness
```

### E5 — Azure `locked/unlocked` != S3 `Compliance/Governance`

Both providers expose WORM-oriented control states, but the names and authorization transitions are not interchangeable.

- S3's launch/current contract distinguishes Governance bypass authority from Compliance protection.
- Azure documents a lock transition governing whether an immutability policy can be shortened/deleted, along with separate scope/default/inheritance rules.

No inspected source establishes a one-to-one mapping such as:

```text
Azure unlocked = S3 Governance
Azure locked   = S3 Compliance
```

That tempting translation is explicitly rejected. The useful comparison is only that **retention policy itself can be retained under an authority regime**.

### E6 — WORM relation != version-history relation

P3/P4 separate Blob versioning from immutability. Versioning can preserve predecessor states; WORM policy additionally constrains their mutation/deletion admissibility.

This mirrors the methodological separation already made between Cases 109 and 110, but it does not make Azure's version/delete semantics identical to S3 delete markers.

In particular, P4 describes deletion of an Azure current blob version by moving it into previous-version status; that is not evidence for an S3-style delete-marker object in Azure.

## Cross-provider relation table

| Relation | Azure 18-Sep-2018 GA | Azure current version-level WORM | S3 Object Lock 26-Nov-2018 / current Case 110 |
| --- | --- | --- | --- |
| Provider vocabulary | `WORM`, `immutable` | `version-level WORM`, immutability policy | `Object Lock`, `WORM` |
| Bounded policy scope established here | container | account/container/version with inheritance | object version, with bucket defaults/current docs |
| Versioning dependency | not part of the 2018 container-scope claim | required for version-level WORM | Object Lock works with S3 Versioning |
| Time-based retention | yes | yes | yes |
| Legal hold | yes | yes | yes |
| Policy-authority state | lock/extend operations named at container scope; exact 2018 state machine not reconstructed here | explicit `unlocked -> locked`, locked extension-only | Governance/Compliance have distinct bypass authority |
| Later write at same logical name | not generalized from the 2018 container contract | creates a new version | later version can coexist with protected predecessor |
| Physical write-once medium proven | no | no | no |

This table is a **functional contract comparison**, not a shared implementation diagram or a genealogy.

## Prior-art / novelty boundary

Case 110 previously used ECMA-153 (1994) to prove only the broad point that WORM storage long predates S3 Object Lock. P1/P2 now add a closer floor:

```text
physical optical WORM standardized by 1994
    -> chronological floor only

Azure cloud Blob WORM public preview / GA by Jun/Sep 2018
    -> same broad service class, still no genealogy

AWS S3 Object Lock public launch Nov 2018
```

The contribution of Case 110 is therefore **not** “inventing WORM in cloud object storage.” Its defensible retention-specific value is the exact decomposition of version identity, currentness, retention deadline, legal hold, authorization/bypass state, Lifecycle, and later physical-forgetting boundaries in the S3 contract, now stress-tested against a non-AWS provider whose WORM granularity and control state evolved differently.

## Philosophical interpretation — bounded

### I — a retained prohibition can be part of what makes a state persist

The technical fact is narrow: current Azure and S3 contracts can preserve not only payload/version identity but also **rules that forbid or constrain future mutation/deletion operations**. In Azure's current contract, even the mutability of the retention rule has a one-way locked transition.

This supports one limited conceptual point:

> technical retention can include retained conditions on what future operations are allowed to count as legitimate change.

The interpretation stops at the service contract. It does **not** make an immutability policy a physical force, a proof of unchanged backend cells, a universal archive, `Bestand`, or automatically a Stieglerian tertiary retention.

## Source-bounded negative claims

This deepening does **not** establish:

- Azure or AWS invention priority for WORM, cloud WORM, legal holds, or immutable object storage;
- a direct Azure -> AWS, AWS -> Azure, or shared implementation genealogy;
- equivalence of Azure `locked/unlocked` and S3 Governance/Compliance;
- that Azure's current version-level semantics existed in the June/September-2018 container-level feature;
- that an Azure immutable blob or S3 locked object is stored on physically write-once media;
- backend replica/erasure-coding topology;
- physical movement, overwrite, key retirement, reclamation, or sanitization after service-level retirement;
- exact crash/partition/failover behavior of policy-state replication;
- Google Cloud Storage or on-premises object-lock equivalence;
- regulatory sufficiency for a particular deployment.

## Cross-repository check

A fresh search of `tmzncty/computing-archaeology` for Azure Blob immutability / WORM found no dedicated overlapping study before this pass. Broad cloud-object-storage history, WORM product genealogy, compliance-storage market history, and provider implementation architecture should live there if developed. This evidence file retains only the chronology and policy-state relations needed to sharpen `technical-retention` Case 110.

## Open work

- Reconstruct the Azure 2018 -> version-level-WORM feature chronology from dated release/change records more fully, without treating current documentation as frozen history.
- Compare Google Cloud Storage retention-policy / Bucket Lock / object-retention contracts as a separate named provider slice.
- Investigate current Azure geo-replication/failover wording for immutability-policy changes as a separate distributed control-state persistence case rather than folding it into this WORM-policy slice.
- Add fault/incident evidence where a provider's public contract can be tested against policy migration, failover, or administrative recovery.
- Connect service-level retirement to lower-layer sanitization only where independently documented.

## Research date

Historical and current-contract sources rechecked **2026-09-11**. Current Microsoft Learn semantics are explicitly labeled current and are not silently back-projected into the 2018 launch.
