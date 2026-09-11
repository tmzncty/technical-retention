# Amazon S3 Multipart Upload: Retained Pre-Object Parts, Completion Admission, and Abort Cleanup

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
