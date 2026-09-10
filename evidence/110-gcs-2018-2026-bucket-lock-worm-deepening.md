# Evidence 110 deepening — Google Cloud Storage Bucket Lock, 2018 cloud-WORM prior-art and policy-scope boundary

## Case

[`cases/110-amazon-s3-object-lock-version-worm-retention.md`](../cases/110-amazon-s3-object-lock-version-worm-retention.md)

## Evidence status

**Grounded for a bounded cross-provider public service-contract comparison.**

This pass adds Google Cloud Storage **Bucket Lock** as a second named 2018 hyperscale-cloud comparison to Amazon S3 Object Lock. It intentionally separates three layers:

1. **19–24 October 2018** — Google Cloud's dated feature-availability / GA records for bucket-scoped retention policies and holds;
2. **19 October 2018 historical service terms** — a provider-primary contractual boundary on how Bucket Lock retention related to Project/Account/Agreement lifetime at that date;
3. **current Cloud Storage documentation** — later/current details about retroactivity, Object Versioning interaction, event-based holds, Lifecycle, project liens, and the later Object Retention Lock feature.

Current behavior is not silently projected backward into the 2018 launch. The comparison establishes chronology and retention-policy relations, not provider invention priority, implementation genealogy, backend physical immutability, or regulatory sufficiency.

Claim labels follow [`docs/METHOD.md`](../docs/METHOD.md):

- **H** — historical record;
- **P** — primary/provider documentation;
- **E** — engineering reconstruction from the documented service relation;
- **A** — functional analogy/comparison;
- **I** — bounded philosophical interpretation;
- **X** — explicit exclusion / unsupported stronger claim.

## Sources

### P1 — Cloud Storage release notes, 19 October 2018

Google Cloud, **Cloud Storage release notes**, entry dated **19 October 2018**.

<https://cloud.google.com/storage/docs/release-notes>

The dated entry states that:

- retention policies and object holds were now available;
- a retention policy sets a minimum age before an object may be deleted or overwritten;
- the policy could be locked so it could not be removed or reduced;
- object holds were another way to prevent deletion or overwrite.

Evidence strength: **strong provider-primary dated feature-availability anchor**.

Chronology caution: this entry says the features were “now available.” It is not by itself phrased as a general-availability announcement.

### P2 — Google Cloud Bucket Lock GA announcement, 24 October 2018

Google Cloud Blog, Subhasish Chakraborty, **“Protecting Cloud Storage with WORM, key management and more updates,”** **24 October 2018**.

<https://cloud.google.com/blog/products/storage-data-transfer/protecting-cloud-storage-with-worm-key-management-and-more-updates>

The provider announcement states that:

- Cloud Storage Bucket Lock was **generally available**;
- Google explicitly framed it for `WORM (Write Once Read Many)-compliant or immutable storage`;
- a retention policy defined the retention period for current and future objects in the bucket;
- objects could not be deleted or overwritten before the retention period was satisfied;
- `retention expiration time` metadata exposed when a particular object's period was up;
- a lock prevented reduction of the bucket retention period;
- an object hold retained an object indefinitely;
- event holds could delay the start of a retention period until a later event;
- Lifecycle could move locked data to colder tiers and delete it after the retention period expired.

Evidence strength: **strong provider-primary dated GA/service-contract anchor**.

### P3 — archived Google Cloud Service Specific Terms, 19 October 2018

Google Cloud Platform, **Service Specific Terms**, last modified **19 October 2018** (archived historical version).

<https://cloud.google.com/terms/service-terms-20181019>

Section 3.4 is explicitly specific to Bucket Lock. It states that the customer was responsible for choosing retention/hold periods and keeping the account in good standing, and that upon deletion of a Project or Account, or termination of the Agreement, related Bucket Lock retention/hold periods were no longer in force and Google could delete the applicable data.

Evidence strength: **strong provider-primary historical contractual boundary**.

Important limit: this is legal/service-contract evidence, not a description of backend storage algorithms. It is used only to bound the scope of the 2018 service promise.

### P4 — current Cloud Storage Bucket Lock documentation

Google Cloud, **“Bucket Lock.”**

<https://cloud.google.com/storage/docs/bucket-lock>

Current documentation, last checked 2026-09-11, states that:

- a bucket retention policy applies to existing objects as well as new objects;
- a locked policy cannot be removed or reduced, though it can be increased;
- individual objects expose `retention expiration time` metadata;
- editable object metadata is not itself frozen by the bucket retention policy;
- with Object Versioning, a protected live version may still become noncurrent, and pre-existing versioned objects are also protected when the bucket policy is applied;
- removing an event-based hold resets the object's retention period;
- Lifecycle may be configured but cannot delete an object until retention requirements are satisfied;
- current Bucket Lock applies a project lien intended to block project deletion while the lien remains;
- the account must remain active and in good standing.

Evidence strength: **strong current provider documentation**.

Historical-use limit: these exact current interactions are not assumed to have existed unchanged on 19/24 October 2018.

### P5 — Cloud Storage release notes, 21 November 2023

Google Cloud, **Cloud Storage release notes**, entry dated **21 November 2023**.

<https://cloud.google.com/storage/docs/release-notes>

The dated entry says **Object Retention Lock** became available and describes it as placing a retention configuration on individual objects, optionally locking that configuration so its retain-until date cannot be shortened or removed.

This is used as an anti-anachronism anchor:

```text
2018 Bucket Lock / bucket retention policy
    !=
2023 Object Retention Lock / per-object retention configuration
```

Evidence strength: **strong provider-primary feature-chronology anchor**.

### P6 — inherited comparison anchors

The canonical Case-110 evidence already grounds:

- Microsoft Azure Immutable Blob Storage public preview on **19 June 2018** and GA on **18 September 2018**;
- Amazon S3 Object Lock public launch on **26 November 2018**.

See:

- [`evidence/110-azure-2018-2026-immutable-blob-worm-deepening.md`](110-azure-2018-2026-immutable-blob-worm-deepening.md)
- [`evidence/110-amazon-s3-2018-object-lock-grounding.md`](110-amazon-s3-2018-object-lock-grounding.md)

These dates are reused only for bounded chronology.

## Historical record

### H/P — Google Cloud exposed another public cloud WORM/immutable service before S3 Object Lock

P1 records retention policies and holds as available on **19 October 2018**. P2 calls Bucket Lock **generally available** on **24 October 2018** and explicitly uses WORM/immutable-storage vocabulary. The inherited AWS anchor dates S3 Object Lock's public launch to **26 November 2018**.

The safe chronological conclusion is:

```text
Google Cloud retention-policy/hold availability — 19 Oct 2018
Google Cloud Bucket Lock GA announcement        — 24 Oct 2018
Amazon S3 Object Lock public launch             — 26 Nov 2018
```

Together with Azure's **18 September 2018** GA, this supplies two named same-class cloud-service counterexamples before the dated S3 launch.

It does **not** establish:

- Google or Microsoft invention priority for cloud WORM;
- private-preview/internal-development priority;
- AWS copying either provider;
- causal or code genealogy among the services.

### H/P — availability date != GA-announcement date

P1 and P2 are close but not identical chronology records.

- 19 October: release notes say retention policies and object holds are “now available.”
- 24 October: product blog explicitly announces Bucket Lock as generally available.

The repository therefore retains both dates rather than silently choosing one and calling the other an error.

### H/P — the 2018 Google policy was bucket-scoped

P2 describes a retention policy for **current and future objects in the bucket** and a lock on the **bucket** preventing reduction of the retention period.

That gives a different 2018 granularity from S3 Object Lock's per-object-version contract and from later Google Object Retention Lock. The useful historical claim is only:

> Google Cloud had a bucket-scoped WORM/immutable retention regime in public service by October 2018.

### H/P — 2018 service permanence was still scoped by the provider/account relation

P3 is unusually explicit: at that date, Bucket Lock retention/hold periods were conditioned by the Project/Account/Agreement relation, and deletion of the Project/Account or termination of the Agreement could end those periods.

This does not make the 2018 service “not WORM.” It instead bounds what the provider promise meant:

```text
locked bucket-retention policy
    !=
carrier-independent preservation outside the cloud service/account relation
```

This is a historical contractual fact, not a backend engineering inference.

## Current-contract engineering reconstruction

### E1 — bucket policy scope != version currentness

P4 says a live version whose retention expiration lies in the future may still be made noncurrent under Object Versioning.

Thus:

```text
protected object version remains retained
    !=
that version remains current
```

A bucket-wide policy can constrain deletion/replacement while logical currentness continues to change.

### E2 — retroactive policy attachment != rewriting object age/history

Current Bucket Lock applies to existing as well as future objects. Existing objects become subject to the policy, but their object ages/creation histories are not thereby recreated as new objects.

The control relation can therefore be attached later than the payload:

```text
payload creation time
    !=
retention-policy attachment time
```

This is a service-contract reconstruction, not a claim about internal metadata layout.

### E3 — retention-expiration metadata != deletion event

P2/P4 expose a per-object retention expiration time. Reaching that time changes deletion/replacement **eligibility**; it does not itself prove that a delete, reclamation, key destruction, or media erase occurred.

```text
retention requirement satisfied
    !=
object deleted
    !=
physical sanitization
```

### E4 — locked-policy state != retention-duration value

Current documentation permits increasing a locked bucket's retention period but not reducing/removing it.

The retained control state therefore has at least two separable aspects:

```text
duration / deadline rule
    !=
mutability authority over that rule
```

“Locked” does not mean every field and every related object property becomes forever immutable.

### E5 — payload mutation barrier != metadata immutability

P4 explicitly excludes editable object metadata from the bucket retention policy's mutation barrier.

Thus a protected payload/object generation can coexist with later metadata changes:

```text
content overwrite/delete prohibited
    !=
all associated metadata frozen
```

This is an important counterexample to treating service-level `immutable` as a universal bit-for-bit freeze of every service-visible state.

### E6 — event-hold release != immediate deletion eligibility

P4 states that removing an event-based hold resets the object's retention period.

The hold therefore can be part of the **start condition** for a later fixed retention interval:

```text
hold removed
    !=
retention obligation ended
```

This differs from S3's documented legal-hold relation and should not be normalized into one provider-independent hold state machine.

### E7 — Lifecycle eligibility != retention-policy bypass

P4 permits Object Lifecycle Management alongside Bucket Lock but says Lifecycle cannot delete an object until retention requirements are met.

Therefore:

```text
lifecycle rule matches
    !=
retention barrier overridden
```

The lifecycle policy and the WORM retention policy compose as separate authorities.

### E8 — current project lien is a separate outer control relation

P4 currently documents a project lien applied when a bucket retention policy is locked. The lien blocks project deletion while present; an appropriately authorized project owner or organization administrator can remove it.

This is a higher-level relation around the bucket policy:

```text
object retention state
    !=
bucket policy lock state
    !=
project-deletion admission state
```

The exact date when the lien behavior entered or changed is **not** established by this pass. It must not be projected backward merely because current documentation describes it.

## Cross-provider comparison

| Relation | Azure Immutable Blob GA 18-Sep-2018 | GCS Bucket Lock Oct-2018 | S3 Object Lock 26-Nov-2018 / current Case 110 |
| --- | --- | --- | --- |
| Dated pre-S3 public cloud WORM floor | yes | yes | launch anchor |
| 2018 policy granularity established here | Blob Container | bucket | object version |
| Provider WORM/immutable vocabulary | yes | yes | yes |
| Time-based retention | yes | yes | yes |
| Hold relation | legal hold | temporary/event holds in launch material | legal hold |
| Later version/per-object layer | version-level WORM is later | Object Retention Lock appears in 2023 | Object Lock is version-scoped |
| Exact authority state machine identical | no | no | no |
| Backend physical write-once media proven | no | no | no |

This is a **functional service-contract comparison**, not a shared implementation diagram or genealogy.

### A — common “WORM” vocabulary != common scope or authority semantics

All three providers use WORM/immutable language around cloud object/blob storage, but the bounded records already show different granularity and state evolution.

Therefore:

```text
same marketing/engineering category
    !=
same protected object identity
    !=
same bypass/lock/hold state machine
    !=
same backend mechanism
```

### A — later GCS Object Retention Lock must not be back-projected into 2018

P5 places per-object **Object Retention Lock** availability at **21 November 2023**. Current Google documentation may now discuss Bucket Lock and Object Retention Lock together, but the 2023 chronology blocks the shortcut:

```text
current GCS per-object retention contract
    !=
2018 Bucket Lock semantics
```

That is directly parallel to the Azure anti-anachronism guardrail already added to Case 110, but it is independently sourced.

## Philosophical interpretation — bounded

### I — retained prohibition can depend on retained institutional relations

The engineering/service fact is limited: cloud WORM retention can include control state that constrains future mutation, while the historical Google terms also make that promise dependent on an ongoing Project/Account/Agreement relation.

A cautious interpretation is:

> some technical retention at infrastructure scale is constituted not only by payload and controller policy, but also by retained administrative/institutional relations that keep the policy operative.

This should not be inflated into a claim that legal terms are a storage substrate, that policy is a physical force, or that every archive is reducible to account state.

## Source-bounded negative claims

This deepening does **not** establish:

- Google, Microsoft, or AWS invention priority for WORM or cloud WORM;
- direct Azure→Google→AWS, Google→AWS, AWS→Google, or shared implementation genealogy;
- exact Google private-preview chronology before 19 October 2018;
- that current Bucket Lock semantics were unchanged since launch;
- that current project-lien behavior existed in October 2018;
- equivalence of GCS object holds and S3/Azure legal holds;
- equivalence of current GCS Object Retention Lock and S3 Object Lock;
- backend replica/erasure-coding topology;
- physical write-once media, key-retirement behavior, reclamation, or sanitization;
- regulatory sufficiency for a particular deployment;
- fault/partition/failover behavior of retention-policy replication.

## Cross-repository check

Fresh searches of `tmzncty/computing-archaeology` for `Bucket Lock` and `Google Cloud Storage retention policy` found no dedicated overlapping study before this pass.

Broader cloud-storage product history, WORM genealogy, compliance-storage market history, and provider implementation architecture should live there if developed. This evidence file retains only the chronology and retention-policy relations needed to sharpen Case 110.

## Open work

- Recover any pre-19-October-2018 Google preview/private-public chronology from dated primary records before making an earlier availability claim.
- Reconstruct the exact historical introduction of project-lien behavior rather than projecting current documentation backward.
- Compare an on-premises object-lock/WORM implementation as a separate slice.
- Add incident/fault evidence for policy migration, administrative recovery, account closure, or failover where primary evidence permits.
- Connect service-level retirement to lower-layer sanitization only where independently documented.

## Research date

Historical and current provider sources rechecked **2026-09-11**. Current Google Cloud semantics are explicitly labeled current and are not silently back-projected into the 2018 launch.
