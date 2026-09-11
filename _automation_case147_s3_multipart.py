from pathlib import Path

CASE_PATH = Path('cases/147-s3-multipart-upload-preobject-retention.md')
EVIDENCE_PATH = Path('evidence/147-s3-2010-2016-multipart-preobject-retention-grounding.md')
INDEX_PATH = Path('CASE_INDEX.md')
ROADMAP_PATH = Path('ROADMAP.md')

for p in (INDEX_PATH, ROADMAP_PATH):
    if not p.exists():
        raise SystemExit(f'missing required file: {p}')
for p in (CASE_PATH, EVIDENCE_PATH):
    if p.exists():
        raise SystemExit(f'{p} already exists; refusing duplicate/concurrent integration')

CASE = r'''# Amazon S3 Multipart Upload: Retained Pre-Object Parts, Completion Admission, and Abort Cleanup

## Status

**`grounded`** — bounded to Amazon S3's first-party 10-Nov-2010 Multipart Upload launch record, current AWS API/User Guide semantics for in-progress uploads, parts, completion, and abort, plus the dated 16-Mar-2016 introduction of lifecycle-driven incomplete-upload expiration.

Grounding record: [`../evidence/147-s3-2010-2016-multipart-preobject-retention-grounding.md`](../evidence/147-s3-2010-2016-multipart-preobject-retention-grounding.md).

## Scope

This case asks a narrow distributed/object-storage question:

> What state can S3 retain after bytes have been accepted and stored but before an object has been created, and what relation makes those stored parts later count as one object or instead become cleanup candidates?

The bounded mechanism is:

```text
CreateMultipartUpload
    -> upload ID / in-progress upload relation
    -> independently stored parts + part numbers + ETags
    -> either:
         CompleteMultipartUpload -> object/version creation
       or
         AbortMultipartUpload -> upload retired + part storage cleanup
       or
         later lifecycle eligibility -> service-driven abort/cleanup
```

This is **not**:

- a general history of Amazon S3;
- a claim that AWS invented multipart transfer, resumable upload, staged object construction, garbage collection, or transaction commit;
- evidence about S3's undisclosed backend chunk placement or replica layout;
- a claim that multipart parts are normal S3 objects or object versions before completion;
- a claim that aborting an upload securely sanitizes every physical embodiment of a part;
- a claim that one successful Abort request proves all racing part writes have already disappeared;
- a claim that lifecycle expiration of incomplete multipart uploads is object expiration.

The contribution is a bounded **pre-object retention / admission / cleanup relation** at the S3 service interface.

---

## Historical vocabulary and chronology

AWS announced **Amazon S3 Multipart Upload on 10 November 2010**. The launch announcement says a client can upload a single object as a set of parts, pause/resume the upload, and begin before total object size is known. Jeff Barr's same-day AWS News Blog describes initiation returning an `upload id`, independent part uploads, and a final request asking S3 to assemble the object.

For this case, 10-Nov-2010 is therefore a public service/feature anchor. It is **not** an invention-priority claim. No direct genealogy is inferred from older multipart transfer protocols or storage systems merely because they share staged-transfer functions.

AWS separately announced **new S3 Lifecycle policies on 16 March 2016**, including an incomplete multipart upload expiration policy. That dated record says incomplete partial uploads do not appear in ordinary object listings by default but still incur storage charges, and that the new policy can automatically expire them after a predefined number of days, including existing partial uploads.

Therefore:

> `2010 multipart-upload launch != 2016 lifecycle auto-abort feature`.

Current AWS documentation is used below to define the maintained service contract. Current semantics are not silently projected into every detail of the 2010 launch implementation.

---

## Retained state

At least five state classes must be distinguished:

1. **uploaded part payload** — bytes accepted for one part;
2. **multipart-upload identity/control state** — bucket/key plus an upload ID that qualifies subsequent UploadPart/ListParts/Complete/Abort operations;
3. **part ordering/currentness state** — part number and returned ETag used to identify the parts selected at completion;
4. **final object/object-version state** — created only after successful completion;
5. **cleanup/lifecycle state** — abort eligibility and service-side retirement of the incomplete upload and its parts.

These are not one thing.

The current User Guide is explicit that S3 retains uploaded parts until the upload is completed or stopped, and bills for their storage during that lifetime. Yet AWS's abort guidance separately says S3 creates the object only after successful completion.

Therefore:

> **stored/billed part bytes != created object**.

A service can retain substantial payload before that payload has been admitted as the named object the client ultimately intends to create.

---

## Identity and addressing

### Upload ID is pre-object operation identity

Current `UploadPart` and `ListParts` API documentation requires the `uploadId` returned by initiation. `ListMultipartUploads` defines an in-progress multipart upload as one initiated but not yet completed or aborted.

The object key alone therefore does not uniquely identify one in-progress construction. The retained upload relation includes the upload ID.

> **object key != multipart-upload identity**.

Multiple construction attempts can target a key without their parts becoming one undifferentiated pool.

The upload ID is control/identity metadata, not a replica of the eventual object's payload.

### Part number is position and currentness within one upload

Current `UploadPart` documentation says a part number identifies a part and determines its position in the object being created; uploading a new part with a part number already used replaces the previously uploaded part for that number.

Thus even before object creation there is a bounded currentness relation:

> **all historically uploaded part payloads != the part set admitted at completion**.

An earlier physical/service-retained part can become superseded inside the in-progress construction before any final object exists.

### ListParts is retained construction evidence, not completion authority by itself

`ListParts` exposes uploaded parts for a specific upload ID. Current S3 guidance nevertheless warns not to use the result of the listing as the authoritative input for `CompleteMultipartUpload`; clients should retain the part numbers and ETags returned by their upload operations.

So:

> **server-visible part listing != client-maintained completion manifest**.

Both concern the same in-progress construction, but they have different operational roles.

---

## Completion: stored parts become one admitted object

Current `CompleteMultipartUpload` documentation says S3 concatenates the supplied parts in ascending part-number order and creates a new object. If bucket versioning is enabled, the current API can return the version ID of the newly created object.

The important relation is not merely physical concatenation. At the S3 contract boundary, successful completion changes what the service recognizes:

```text
retained parts under upload ID
    !=
ordinary object/version

successful CompleteMultipartUpload
    ->
new object/version admitted under bucket + key
```

Therefore:

> **payload storage != namespace/object admission**.

And:

> **completion relation != proof of one particular backend physical assembly**.

AWS may implement the service with undisclosed internal layouts; the interface claim is only that the specified parts become the newly created S3 object in the documented order.

This sharply complements Case 109. S3 Versioning governs already created object versions and their currentness; Case 147 isolates state that can be retained **before any new object version is created by the multipart operation**.

---

## Abort: retiring construction authority and reclaiming part storage

Current `AbortMultipartUpload` documentation says that after an upload is aborted, no additional parts can be uploaded using that upload ID and storage consumed by previously uploaded parts is freed.

At the logical/service level this creates two linked transitions:

1. the upload ID ceases to authorize further construction work;
2. associated part storage becomes cleanup/reclamation work.

So:

> **abort of construction authority != object deletion**.

There may never have been a completed object for this upload to delete.

This also means:

> **incomplete-upload cleanup != object lifecycle expiration**.

AWS's lifecycle documentation explicitly says `AbortIncompleteMultipartUpload` does not apply to objects and deletes no objects.

---

## Abort is not an instantaneous cleanup proof under racing writes

The strongest counterexample in the current API is the documented race around Abort.

AWS says part uploads already in progress when `AbortMultipartUpload` is issued **might or might not succeed**. The API documentation therefore warns that a multipart upload may need to be aborted multiple times to free all part storage, and recommends `ListParts` to verify that the parts list is empty.

This gives a precise state-transition distinction:

> **Abort request/response != verified exhaustion of all part storage**.

And more generally:

> **authority retirement can precede verified material/service cleanup**.

A racing UploadPart can have begun under still-valid authority and finish after an abort transition. The service contract therefore exposes cleanup as a condition that may need subsequent observation, not merely a Boolean inferred from one command response.

This is not evidence that S3 violates its contract. The race and the verification procedure are part of the documented contract.

---

## Time and lifecycle policy

Before the lifecycle feature, abandoned multipart uploads could remain stored/billed until clients explicitly completed or aborted them. AWS's 16-Mar-2016 announcement added a policy that makes an incomplete multipart upload eligible for automatic expiration after a configured number of days.

Current lifecycle documentation preserves the same basic relation: age is measured from **multipart-upload initiation**, and once the configured interval is exceeded, S3 can abort the incomplete upload and delete associated parts.

Thus:

> **incomplete-upload age != object age**.

The timer begins before an object necessarily exists.

Also:

> **age threshold != immediate physical erasure instant**.

The service-level policy establishes eligibility/cleanup behavior; it does not expose exact backend media-reclamation or sanitization timing.

The 2016 announcement says the policy also applies to existing partial uploads. Therefore a later policy can impose a retirement rule on pre-existing in-progress constructions without converting them into objects first.

---

## Maintenance and invisible work

Multipart upload creates background/service obligations that ordinary object listing can hide:

- retain uploaded parts;
- retain upload identity and part metadata;
- accept/retry independent part writes;
- expose `ListParts` / `ListMultipartUploads` state;
- on completion, validate the supplied part set and create the object;
- on abort/lifecycle cleanup, retire the construction and reclaim part storage;
- account/bill storage while the upload remains incomplete.

This is a useful distributed-storage retention case because **not appearing as an ordinary object does not imply absence of retained storage state**.

In-progress uploads are explicitly listable through their own API and can consume storage/cost while remaining outside ordinary object creation.

---

## Failure and forgetting boundaries

Keep the following distinct:

- **network/application interruption** — uploaded parts can remain available for later continuation;
- **failed individual part upload** — that part can be retransmitted without restarting already successful parts;
- **incomplete multipart upload** — initiation occurred, completion/abort has not retired the relation;
- **successful completion** — selected parts become a created object/version;
- **abort** — the construction is retired and part cleanup is requested/performed under the documented race semantics;
- **lifecycle auto-abort** — age/policy drives retirement of incomplete uploads;
- **object deletion/version expiration** — acts on created objects/versions, not the same state class;
- **media sanitization** — not established by any multipart abort/cleanup document used here.

Especially:

> **service says storage is freed != forensic proof every lower-layer embodiment is sanitized**.

Case 44 remains the repository's bounded NVMe deallocate/sanitize boundary; Case 147 should not turn a cloud-service cleanup statement into a physical-erasure claim.

---

## Engineering reconstruction

The bounded source set supports the following decomposition:

```text
part bytes retained
    !=
pre-object construction identity
    !=
selected completion manifest
    !=
created object/version
    !=
cleanup eligibility
    !=
verified part-storage exhaustion
    !=
physical-media sanitization
```

The case adds a useful kind of retained state to the project: **prospective payload that is durable enough to continue a future construction but is not yet admitted as the final named object**.

A compact invariant is:

> **A system can retain the material of a possible future object without yet retaining that object as a current namespace entity.**

That is project engineering language, not AWS historical vocabulary.

---

## Functional comparisons

### Case 109 — S3 Versioning

Case 109 concerns current/noncurrent versions after object creation. Case 147 concerns uploaded parts before completion creates a new object/version.

> `pre-object construction state != noncurrent object version`.

### Case 143 — SQLite rollback journal

Both cases retain substantial payload outside the ordinary final/current state boundary, but their direction is opposite:

- SQLite rollback journal retains **prior** page state so an interrupted update can be undone;
- S3 multipart upload retains **prospective** part state so a future object can be completed.

The comparison is functional only. No genealogy is implied.

### Case 146 — Flash erase suspend

Both cases show unfinished work can remain current across an interruption, but the retained state differs radically. Flash erase suspend retains device operation/admission state while one physical erase is paused. S3 retains uploaded payload parts plus a service-level construction identity across application/network gaps.

> `unfinished-work continuity != one universal checkpoint mechanism`.

### Case 73 — GFS lazy garbage collection

Both expose delayed reclamation, but GFS garbage collection concerns namespace-disconnected/dead chunks after file/chunk-state transitions, whereas S3 incomplete-upload lifecycle cleanup retires prospective parts that never became the completed object. Shared cleanup shape is not identical currentness semantics.

---

## Prior art and anti-anachronism

The safe historical claims are deliberately narrow:

- AWS publicly launched S3 Multipart Upload on 10-Nov-2010;
- the launch record already documents upload IDs, independently uploaded parts, and a final assembly request;
- AWS launched incomplete-multipart lifecycle expiration on 16-Mar-2016.

This case does **not** claim:

- 2010 as invention of multipart/resumable transfer;
- 2016 as invention of age-based garbage collection;
- current API race wording existed verbatim in 2010;
- the current maximum part count, checksum model, directory-bucket semantics, or version-ID behavior should be back-projected into the launch contract;
- any direct lineage from database transactions, filesystems, Flash GC, or earlier distributed stores.

A broader multipart-transfer/object-store genealogy belongs primarily in `computing-archaeology`.

---

## Philosophical limit

A narrow interpretive pressure follows from the engineering relation:

> Technical existence can be typed: bytes may be retained, addressable through a construction protocol, and economically chargeable while still not counting as the final object they are intended to become.

This is useful because it separates **material/service persistence** from **object admission/currentness**.

The analogy stops there. An incomplete multipart upload is not a metaphysical “potential object,” a memory in the human sense, or evidence for a general ontology of becoming. AWS documents a concrete service protocol with explicit initiation, part identity, completion, abort, and lifecycle rules.

---

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| AWS publicly announced S3 Multipart Upload on 10-Nov-2010 | H/P | first-party launch announcement/blog |
| The launch design uses initiation/upload ID, independent part uploads, and a final completion/assembly step | H/P | first-party launch blog |
| Current S3 retains/bills uploaded parts until completion or abort | H/P | current AWS User Guide |
| Stored multipart parts are not yet the completed object | H/P, E | AWS abort/overview docs |
| Upload ID is required to address one in-progress upload's parts | H/P | current UploadPart/ListParts APIs |
| Re-uploading the same part number replaces that part within the in-progress upload | H/P | current UploadPart API |
| CompleteMultipartUpload creates the new object from the supplied ordered part set | H/P | current Complete API |
| One Abort response always proves every racing part has vanished | X | contradicted by current Abort API |
| Empty ListParts can be used to verify all part storage is removed after abort | H/P | current Abort API |
| AWS introduced lifecycle expiration for incomplete multipart uploads on 16-Mar-2016 | H/P | dated first-party announcement/document history |
| AbortIncompleteMultipartUpload deletes ordinary S3 objects | X | current lifecycle docs explicitly deny this |
| Service cleanup proves secure physical sanitization | X | not established by source set |
| AWS invented multipart/resumable upload | X | not established |

---

## Related repositories

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `multipart` returned no dedicated study to reuse. A broader history of multipart transfer, resumable uploads, S3 API evolution, or internal object-store implementation should be routed there if developed comprehensively. Case 147 keeps the retention-specific pre-object/currentness/cleanup relation.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) remains the methodological guard against turning a 2010 public launch date into invention priority or silently treating maintained 2026 documentation as the verbatim 2010 contract.

---

## Sources

1. Amazon Web Services, **Introducing Amazon S3 Multipart Upload**, 10 Nov 2010: <https://aws.amazon.com/about-aws/whats-new/2010/11/10/Amazon-S3-Introducing-Multipart-Upload/>.
2. Jeff Barr, AWS News Blog, **Amazon S3: Multipart Upload**, 10 Nov 2010: <https://aws.amazon.com/blogs/aws/amazon-s3-multipart-upload/>.
3. Amazon S3 User Guide, **Uploading and copying objects using multipart upload in Amazon S3**: <https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html>.
4. Amazon S3 API Reference, **UploadPart**: <https://docs.aws.amazon.com/AmazonS3/latest/API/API_UploadPart.html>.
5. Amazon S3 API Reference, **ListParts**: <https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListParts.html>.
6. Amazon S3 API Reference, **ListMultipartUploads**: <https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListMultipartUploads.html>.
7. Amazon S3 API Reference, **CompleteMultipartUpload**: <https://docs.aws.amazon.com/AmazonS3/latest/API/API_CompleteMultipartUpload.html>.
8. Amazon S3 API Reference, **AbortMultipartUpload**: <https://docs.aws.amazon.com/AmazonS3/latest/API/API_AbortMultipartUpload.html>.
9. Amazon Web Services, **Introducing new Amazon S3 Lifecycle Policies**, 16 Mar 2016: <https://aws.amazon.com/about-aws/whats-new/2016/03/introducing-new-amazon-s3-lifecycle-policies/>.
10. Amazon S3 User Guide, **Configuring a bucket lifecycle configuration to delete incomplete multipart uploads**: <https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpu-abort-incomplete-mpu-lifecycle-config.html>.
11. Amazon S3 User Guide, **Document history**, entry for 16 Mar 2016: <https://docs.aws.amazon.com/AmazonS3/latest/userguide/WhatsNew.html>.
'''

EVIDENCE = r'''# Case 147 grounding — Amazon S3 multipart upload pre-object retention (2010–2016, maintained contract)

## Purpose

This record grounds one bounded relation for Case 147:

> Amazon S3 can retain and bill uploaded part payload under an in-progress multipart-upload identity before a final object exists; successful completion admits selected parts as a new object, while abort/lifecycle rules retire the in-progress construction and reclaim service-level part storage under a documented race boundary.

The evidence is intentionally split into dated historical records and maintained/current API documentation. Current contract details are not projected backward into the 2010 launch.

## Source classification

| Source | Date / status | Class | Use |
| --- | --- | --- | --- |
| AWS “Introducing Amazon S3 Multipart Upload” | 10-Nov-2010 | `H/P` | public service launch; staged part upload and final object presentation |
| Jeff Barr, AWS News Blog “Amazon S3: Multipart Upload” | 10-Nov-2010 | `H/P` | launch workflow: initiate/upload ID, independent parts, finalize |
| S3 multipart User Guide | maintained/current, accessed 2026-09-11 | `H/P` current contract | retained/billed part lifetime; completion; listing boundary |
| `UploadPart`, `ListParts`, `ListMultipartUploads`, `CompleteMultipartUpload`, `AbortMultipartUpload` API refs | maintained/current, accessed 2026-09-11 | `H/P` current contract | identity/currentness/completion/abort race semantics |
| AWS “Introducing new Amazon S3 Lifecycle Policies” | 16-Mar-2016 | `H/P` | dated launch of incomplete-multipart expiration policy |
| S3 document history | maintained record with 16-Mar-2016 entry | `H/P` | independent AWS documentation of lifecycle action introduction |
| lifecycle incomplete-multipart User Guide | maintained/current | `H/P` current contract | age-based eligibility and object/non-object boundary |

No PDF OCR or screenshot-derived text is used in this evidence record.

---

## 1. 10-Nov-2010 historical launch anchor

AWS's first-party What's New item is dated **Nov 10, 2010** and announces Multipart Upload as a new S3 feature. It describes one object being uploaded as a set of parts and says that after all parts are uploaded S3 presents the data as a single object. It also advertises pause/resume and beginning before total object size is known.

Jeff Barr's same-day AWS News Blog supplies more operational detail. The launch workflow includes:

1. initiate multipart upload and receive an **upload id**;
2. upload chunks independently with the upload id and part number;
3. retain the returned ETag for each part;
4. finalize by sending upload id plus selected part-number/ETag pairs so S3 assembles the object.

### Supported historical claims

- `H/P`: S3 Multipart Upload was publicly launched by 10-Nov-2010.
- `H/P`: the public launch already exposed a distinct initiation identity and independently retained parts before final assembly.
- `H/P`: finalization/assembly was a separate request after part transfer.

### Unsupported escalation

- `X`: AWS invented multipart upload or resumable transfer.
- `X`: every current API detail existed unchanged on launch day.
- `X`: current backend implementation can be inferred from the 2010 interface description.

The launch blog has been maintained over time, so exact numeric limits or ancillary current wording are not used here as immutable 2010 historical facts unless independently anchored.

---

## 2. Current retained-part lifetime: stored and billed before object creation

The maintained S3 multipart-upload overview states that after initiation and one or more successful part uploads, the client must either complete or stop the multipart upload to stop incurring storage charges for the uploaded parts. It says S3 retains the parts throughout the in-progress upload lifetime.

The abort guide separately states that S3 stores uploaded parts and **only creates the object after** the parts are uploaded and a successful completion request is sent. Without successful completion, S3 does not assemble/create the object.

This pair directly grounds:

> **stored/billed part bytes != completed object**.

The service has a state class that is materially/economically retained but not yet an ordinary created S3 object.

This is stronger than a generic client-side “temporary file” analogy because the storage/billing and construction identity are service-side contract facts.

---

## 3. Upload ID and part number are constitutive pre-object identity/currentness state

Current `UploadPart` says the client must first initiate a multipart upload and include the returned unique upload ID with each part request.

Current `ListParts` likewise requires the upload ID to enumerate parts of one specific multipart upload. `ListMultipartUploads` defines in-progress uploads as initiated but neither completed nor aborted.

Therefore:

- `object key != in-progress-upload identity`;
- `upload ID != payload replica`;
- `initiation state != object creation`.

`UploadPart` additionally says part number identifies a part/position and that uploading a new part with a number already used overwrites the previously uploaded part for that number.

Therefore:

> **historically accepted part payload != currently selected part payload for that part number**.

Pre-object state can already have supersession/currentness before the final object exists.

---

## 4. Completion is an admission/currentness transition

Current `CompleteMultipartUpload` says S3 completes the upload by concatenating the supplied parts in ascending part-number order and creates a new object. The caller supplies each selected PartNumber and ETag.

If versioning is enabled, the current API can return the version ID of the newly created object.

The safe engineering reconstruction is:

```text
uploaded part embodiments + upload relation
    --successful completion-->
new service-recognized object/version
```

This does **not** imply that S3 must physically concatenate all bytes into one contiguous backend extent. The interface establishes object creation/admission and logical ordering, not internal media layout.

### Listing counterexample

The current multipart overview warns that `ListParts` should be used for verification and says clients should maintain the part numbers and ETags returned by their own UploadPart calls rather than use a listing result as the completion request's source of truth.

Thus:

> `service listing evidence != client completion manifest authority`.

The same retained construction is viewed through different operational evidence paths.

---

## 5. Abort retires upload authority but has a documented cleanup race

Current `AbortMultipartUpload` says:

- after abort, additional parts cannot be uploaded using that upload ID;
- storage consumed by previously uploaded parts is freed;
- **however**, part uploads already in progress might still succeed or fail;
- as a result, it may be necessary to abort a given multipart upload multiple times to completely free all part storage;
- clients should call `ListParts` and ensure the list is empty to verify removal and avoid further charges.

This is the strongest bounded transition evidence in the slice.

It supports:

> **authority retirement != instantaneous verified cleanup**.

And:

> **Abort response != proof that every racing part write has already ceased to consume storage**.

The API explicitly makes later observation (`ListParts` empty) a stronger cleanup witness than assuming one Abort call collapsed every concurrent state transition at the same instant.

This is a service-level race/admission fact. No claim is made about the exact physical deletion schedule of replicas or media pages.

---

## 6. 16-Mar-2016 lifecycle policy adds time-based retirement of incomplete work

AWS's dated **16 March 2016** What's New post announces two new lifecycle policies. The first is an **incomplete multipart upload expiration policy**.

The post explicitly says:

- an incomplete partial upload does not appear when ordinary objects are listed by default;
- it still incurs storage charges;
- previously clients needed to cancel uploads manually to remove partial uploads;
- from that date a lifecycle policy could automatically expire incomplete multipart uploads after a predefined number of days;
- the policy also applies to existing partial uploads.

AWS's S3 document history independently records the 16-Mar-2016 lifecycle enhancement and names the `AbortIncompleteMultipartUpload` action.

Current lifecycle documentation says age is counted from multipart-upload initiation; after the specified period the upload becomes eligible for abort, S3 stops it, and associated parts are deleted.

It also explicitly states that this action **doesn't apply to objects** and deletes no objects.

This grounds:

> `incomplete-upload retention age != object retention age`;

and:

> `AbortIncompleteMultipartUpload != object expiration`.

The lifecycle rule governs unfinished construction state that can exist before the target object exists.

---

## 7. Failure/forgetting stop conditions

### Network or client interruption

The 2010 launch rationale emphasizes retrying failed chunks and pause/resume rather than restarting the entire object transfer. Successful parts can therefore outlive one client/network attempt.

`connection lifetime != multipart-upload lifetime` is a safe functional statement at this service boundary, although no claim is made that every abandoned upload is retained forever.

### Incomplete != absent

The 2016 announcement's billing/listing contrast supplies a direct counterexample:

> **not present in ordinary object listings != no service-retained payload**.

### Abort != completed object deletion

No completed object need exist. The cleanup target is the in-progress upload/parts state.

### Service deletion != secure sanitization

The sources say service storage is freed/deleted after abort or lifecycle cleanup. They do not establish overwrite, NAND block erase, cryptographic key destruction, replica-by-replica purge timing, or forensic irrecoverability.

Case 44/47 remain the repository's stronger sanitize/remanence boundaries.

---

## 8. Cross-case boundaries

### Case 109: S3 Versioning

Case 109 begins from created object versions. Case 147 demonstrates a prior state class whose bytes can already be stored while no new object version has yet been created by the multipart operation.

`in-progress part != noncurrent version`.

### Case 143: SQLite rollback journal

SQLite retains old page state to make rollback possible; S3 retains future-object parts to make completion possible. Both are non-final payload around an authority transition, but the temporal direction and protocol are different.

Functional analogy only; no genealogy.

### Case 146: Flash erase suspend

Both retain unfinished-work identity across a pause, but one is a distributed service construction with retained part payload while the other is a device state-machine relation around an in-progress physical erase.

`unfinished work continuity != universal checkpoint mechanism`.

### Case 73: GFS garbage collection

Both can reclaim state only after a higher-level relation changes, but GFS dead-chunk GC concerns former/current namespace content while S3 incomplete-upload cleanup concerns prospective payload not yet admitted as the final object.

`reclamation shape != same retained-state class`.

---

## 9. Related-repository check

A fresh GitHub search of `tmzncty/computing-archaeology` for **`multipart`** returned no dedicated study to reuse on 2026-09-11.

Broad S3/API history, multipart transfer genealogy, HTTP upload history, client library evolution, and backend object-store implementation should live primarily there if developed. This record stays with the retention-specific relation among pre-object payload, upload identity, completion authority, abort cleanup, and lifecycle aging.

---

## 10. Claim matrix

| Claim | Label | Strength |
| --- | --- | --- |
| S3 Multipart Upload public launch is dated 10-Nov-2010 | `H/P` | direct first-party launch record |
| Launch workflow distinguishes upload initiation/ID, parts, and finalization | `H/P` | direct first-party launch blog |
| Current S3 stores/bills successful parts until complete/abort | `H/P` | direct maintained service docs |
| Successful part storage means the final object already exists | `X` | directly contradicted by abort/overview docs |
| Upload ID qualifies one in-progress construction | `H/P` | current API refs |
| Same part number can supersede an earlier uploaded part | `H/P` | current UploadPart API |
| Complete creates a new object from supplied ordered parts | `H/P` | current Complete API |
| One Abort response always proves all racing part storage is gone | `X` | directly contradicted by Abort API |
| Empty ListParts is a documented verification step after abort | `H/P` | current Abort API |
| Incomplete-upload lifecycle expiration was introduced 16-Mar-2016 | `H/P` | dated first-party announcement + doc history |
| Lifecycle incomplete-upload action deletes ordinary objects | `X` | current lifecycle docs reject it |
| Multipart cleanup is secure physical sanitization | `X` | outside source contract |
| AWS invented multipart/resumable transfer | `X` | unsupported priority claim |

---

## Sources

1. AWS, **Introducing Amazon S3 Multipart Upload**, 10-Nov-2010: <https://aws.amazon.com/about-aws/whats-new/2010/11/10/Amazon-S3-Introducing-Multipart-Upload/>.
2. Jeff Barr, AWS News Blog, **Amazon S3: Multipart Upload**, 10-Nov-2010: <https://aws.amazon.com/blogs/aws/amazon-s3-multipart-upload/>.
3. AWS S3 User Guide, **Uploading and copying objects using multipart upload in Amazon S3**: <https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html>.
4. AWS S3 API Reference, **UploadPart**: <https://docs.aws.amazon.com/AmazonS3/latest/API/API_UploadPart.html>.
5. AWS S3 API Reference, **ListParts**: <https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListParts.html>.
6. AWS S3 API Reference, **ListMultipartUploads**: <https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListMultipartUploads.html>.
7. AWS S3 API Reference, **CompleteMultipartUpload**: <https://docs.aws.amazon.com/AmazonS3/latest/API/API_CompleteMultipartUpload.html>.
8. AWS S3 API Reference, **AbortMultipartUpload**: <https://docs.aws.amazon.com/AmazonS3/latest/API/API_AbortMultipartUpload.html>.
9. AWS, **Introducing new Amazon S3 Lifecycle Policies**, 16-Mar-2016: <https://aws.amazon.com/about-aws/whats-new/2016/03/introducing-new-amazon-s3-lifecycle-policies/>.
10. AWS S3 User Guide, **Document history**, 16-Mar-2016 entry: <https://docs.aws.amazon.com/AmazonS3/latest/userguide/WhatsNew.html>.
11. AWS S3 User Guide, **Configuring a bucket lifecycle configuration to delete incomplete multipart uploads**: <https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpu-abort-incomplete-mpu-lifecycle-config.html>.
'''

CASE_ROW = r'''| [Amazon S3 Multipart Upload: Retained Pre-Object Parts, Completion Admission, and Abort Cleanup](cases/147-s3-multipart-upload-preobject-retention.md) | **grounded** | distributed object-store pre-object part payload + upload-ID construction state + explicit completion admission + abort/lifecycle cleanup | distinguish stored/billed bytes from object creation; pre-object part currentness from object-version currentness; abort authority retirement from verified cleanup; incomplete-upload aging from object lifecycle | [2010–2016 + maintained-contract grounding](evidence/147-s3-2010-2016-multipart-preobject-retention-grounding.md); earlier multipart/resumable-transfer genealogy, lifecycle scheduling implementation, backend part/replica embodiment, and physical sanitization remain open |'''

FINDINGS = r'''
## Case 147 — S3 multipart-upload pre-object retention findings

Grounding record: [`evidence/147-s3-2010-2016-multipart-preobject-retention-grounding.md`](evidence/147-s3-2010-2016-multipart-preobject-retention-grounding.md).

- **3175 — 10-Nov-2010 public launch != invention priority:** AWS's dated launch record establishes S3 Multipart Upload as a public service feature by that date, not first invention of multipart/resumable transfer. (`H/P`, `X`)
- **3176 — successful part storage != completed object existence:** current AWS docs say S3 retains/bills uploaded parts while separately saying the object is created only after successful completion. (`H/P`, `E`)
- **3177 — ordinary object-list absence != absence of service-retained payload:** AWS's 2016 launch note says incomplete partial uploads do not appear in ordinary object listings by default yet still incur storage charges. (`H/P`, `E`)
- **3178 — object key != in-progress multipart-upload identity:** current UploadPart/ListParts semantics require the upload ID returned by initiation, so prospective constructions targeting a key remain separately qualified. (`H/P`, `E`)
- **3179 — upload ID/control state != payload replica:** the identifier authorizes/addresses operations over retained parts without being another copy of their bytes. (`E`)
- **3180 — historically uploaded part != currently selected part for a part number:** current UploadPart replaces an earlier part when the same part number is uploaded again, creating pre-object supersession/currentness. (`H/P`, `E`)
- **3181 — part position/currentness != final object currentness:** part numbers order prospective payload within one upload; only completion creates the object/version relation. (`H/P`, `E`)
- **3182 — ListParts evidence != client completion-manifest authority:** maintained AWS guidance treats listing as verification and tells clients to retain their own UploadPart number/ETag results for completion. (`H/P`, `E`)
- **3183 — CompleteMultipartUpload != proof of one backend physical concatenation layout:** the API creates an object from ordered parts but does not expose internal extent/chunk/replica embodiment. (`H/P`, `E`, `X`)
- **3184 — pre-object construction state != noncurrent S3 object version:** Case 109 begins after object-version creation; Case 147 retains prospective payload before the multipart operation creates its new object/version. (`A`, `E`, `X`)
- **3185 — Abort retires upload authority != deleting a completed object:** after abort the upload ID no longer accepts new parts, but the target of this transition is an incomplete construction that may never have produced an object. (`H/P`, `E`)
- **3186 — Abort response != verified exhaustion of racing part storage:** AWS explicitly says in-progress part uploads might succeed/fail after abort and that repeated abort may be needed to free all part storage. (`H/P`, `E`)
- **3187 — empty ListParts is stronger cleanup evidence than assuming one Abort call is instantaneous:** the Abort API recommends verifying that the parts list is empty. (`H/P`, `E`)
- **3188 — authority retirement can precede verified cleanup:** the abort race separates inability to start further work under an upload ID from proof that all previously/racing retained part state has been reclaimed. (`E`)
- **3189 — 2010 multipart launch != 16-Mar-2016 lifecycle auto-abort:** AWS separately dates the incomplete-upload expiration policy, so current lifecycle behavior must not be back-projected into the launch contract. (`H/P`, `X`)
- **3190 — incomplete-upload age != object age:** `AbortIncompleteMultipartUpload` counts days from initiation even though successful object creation may never occur. (`H/P`, `E`)
- **3191 — incomplete-upload lifecycle cleanup != object expiration:** current AWS docs explicitly say this lifecycle action does not apply to objects and deletes no objects. (`H/P`, `E`, `X`)
- **3192 — service part deletion/freeing != secure physical sanitization:** multipart cleanup does not establish overwrite, NAND erase, crypto erase, replica purge timing, or forensic irrecoverability; Cases 44/47 remain the stronger sanitization boundary. (`E`, `A`, `X`)
- **3193 — prospective S3 parts != SQLite rollback journal despite shared non-final payload:** Case 143 retains prior pages for undo while Case 147 retains prospective parts for future construction; comparison is functional only. (`A`, `X`)
- **3194 — unfinished-work continuity != one universal checkpoint mechanism:** S3 retains distributed service payload/identity across client gaps while Case 146 retains device operation state across erase suspension. (`A`, `X`)
- **3195 — related-repository boundary:** fresh `tmzncty/computing-archaeology` search for `multipart` found no dedicated study; broad transfer/S3/API genealogy belongs there, while Case 147 keeps the retention-specific pre-object/admission/cleanup relation. (`H/P` project-state record)
'''

ROADMAP_ENTRY = r'''
- [x] **Case 147 S3 Multipart Upload pre-object retention / completion / abort slice** — [`cases/147-s3-multipart-upload-preobject-retention.md`](cases/147-s3-multipart-upload-preobject-retention.md), grounded by [`evidence/147-s3-2010-2016-multipart-preobject-retention-grounding.md`](evidence/147-s3-2010-2016-multipart-preobject-retention-grounding.md): AWS's 10-Nov-2010 launch record anchors upload-ID/independent-part/finalization semantics, while maintained API docs establish `stored+billed parts != created object`, same-part-number pre-object supersession, explicit completion admission, and the Abort race where authority retirement can precede verified empty-part cleanup. The separately dated 16-Mar-2016 lifecycle feature adds age-based retirement of incomplete uploads and explicitly remains distinct from object expiration. Earlier multipart/resumable-transfer genealogy, backend part/replica embodiment, lifecycle scheduling internals, and physical sanitization remain open; a fresh `computing-archaeology` search found no dedicated multipart study to reuse.
'''

# Create canonical case/evidence files.
CASE_PATH.write_text(CASE.rstrip() + '\n', encoding='utf-8')
EVIDENCE_PATH.write_text(EVIDENCE.rstrip() + '\n', encoding='utf-8')

# Integrate one case row before the comparison matrix.
index = INDEX_PATH.read_text(encoding='utf-8')
if '147-s3-multipart-upload-preobject-retention.md' in index:
    raise SystemExit('Case147 already present in CASE_INDEX; refusing duplicate')
marker = '\n---\n\n\n## Comparison matrix — provisional'
if marker not in index:
    raise SystemExit('CASE_INDEX case-table marker not found')
index = index.replace(marker, '\n' + CASE_ROW + marker, 1)
index = index.rstrip() + '\n' + FINDINGS.strip() + '\n'
INDEX_PATH.write_text(index, encoding='utf-8')

roadmap = ROADMAP_PATH.read_text(encoding='utf-8')
if 'Case 147 S3 Multipart Upload pre-object retention' in roadmap:
    raise SystemExit('Case147 already present in ROADMAP; refusing duplicate')
roadmap = roadmap.rstrip() + '\n' + ROADMAP_ENTRY.strip() + '\n'
ROADMAP_PATH.write_text(roadmap, encoding='utf-8')
