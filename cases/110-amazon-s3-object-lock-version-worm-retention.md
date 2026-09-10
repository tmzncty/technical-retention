# Amazon S3 Object Lock: Per-Version WORM Retention, Legal Holds, and Delete-Marker Boundaries

## Status

**`grounded`** for the bounded public service-contract relation described below.

## Scope

- **Object / system:** Amazon S3 general-purpose buckets using S3 Versioning and S3 Object Lock.
- **Historical anchor:** AWS's public announcement of S3 Object Lock on **26 November 2018**.
- **Later contract evidence:** current AWS User Guide documentation is used to clarify the presently documented semantics of per-version retention, Governance/Compliance modes, legal holds, simple versus version-specific deletion, and Lifecycle interaction. Those current details are not silently projected backward as exact 2018 wording.
- **Prior-art floors:** ECMA-153's June 1994 second edition standardizes a magneto-optical WORM cartridge; Microsoft Azure Immutable Blob Storage then supplies a much closer cloud-service floor, with public preview on 19 June 2018 and general availability on 18 September 2018, before AWS's 26 November 2018 Object Lock launch. Neither chronology establishes invention priority or direct genealogy.
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

## Cross-provider historical deepening

### H/P — Azure Immutable Blob Storage: a closer same-class prior-art floor

Microsoft announced **Immutable storage for Azure Storage Blobs** in public preview on **19 June 2018** and general availability on **18 September 2018**, before AWS's dated **26 November 2018** S3 Object Lock announcement. The Azure GA page explicitly uses WORM/immutable vocabulary, documents time-based retention and legal hold, and places the 2018 policy at **Blob Container** scope for existing and new blobs.

This narrows the novelty boundary:

```text
S3 Object Lock public launch in November 2018
    !=
first publicly documented cloud Blob/object WORM service
```

It does **not** establish that Azure invented cloud WORM, that AWS copied Azure, or that the services share an implementation lineage.

### H/P — current Azure version-level WORM is a later contract, not 2018 semantics

Azure Blob versioning became generally available in **August 2020**. Microsoft's current REST documentation gives `2020-06-12` as the API-version floor for blob/snapshot/version immutability policy. Current version-level WORM therefore supplies a later comparison layer rather than a description of the September-2018 container-scoped launch.

Today, Azure documents account/container/version policy scope, version-policy inheritance, legal hold, and a one-way `unlocked -> locked` policy transition. A locked policy can be extended but not shortened or deleted through that path; changing a container/account default does not retroactively rewrite already inherited version policies. Enabling version-level WORM support is also distinct from setting an active policy.

These relations add several bounded comparisons:

```text
WORM capability enabled
    !=
active version retention policy

current default policy
    !=
already inherited version policy

retention deadline
    !=
policy mutability / lock state

protected version identity
    !=
logical blob name frozen against later versions
```

Azure's `locked/unlocked` states are **not** normalized into S3's Governance/Compliance modes. Both are authority relations around retention, but the documented state machines and bypass semantics differ.

### A — provider similarity is functional, not genealogical

The Azure/S3 comparison is useful because both expose service-level WORM while revealing different policy granularity and control-state histories. It is not evidence for shared backend physical media, shared code, causal descent, or identical delete/version semantics. In particular, S3's delete-marker mechanism remains an S3-specific Case-109/110 relation; current Azure documentation describing a deleted current blob becoming a previous version is not evidence for an S3-style delete marker.

Full source mapping and chronology are in [`evidence/110-azure-2018-2026-immutable-blob-worm-deepening.md`](../evidence/110-azure-2018-2026-immutable-blob-worm-deepening.md).

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
- provider-independent equivalence across Azure, GCS, or on-premises object-lock systems; this pass establishes only specific Azure/S3 chronology and contract contrasts, not implementation equivalence;
- invention priority for WORM storage.

## Open work

- Recover a revision-sensitive Object Lock contract chronology from 2018 onward rather than projecting today's options backward.
- Extend the now-grounded Azure comparison to GCS and/or on-premises object-lock systems without flattening version scope, bypass authority, default retention, legal holds, or implementation lineage.
- Add incident/fault evidence for governance bypass, policy misconfiguration, lifecycle interaction, or administrative recovery.
- Connect service-level version retirement to independently documented lower-layer sanitization only where evidence permits.
- Route the broader history of optical, tape, filesystem, and archival WORM mechanisms to `computing-archaeology` rather than duplicating it here.

## Sources

See [`evidence/110-amazon-s3-2018-object-lock-grounding.md`](../evidence/110-amazon-s3-2018-object-lock-grounding.md) and [`evidence/110-azure-2018-2026-immutable-blob-worm-deepening.md`](../evidence/110-azure-2018-2026-immutable-blob-worm-deepening.md).
