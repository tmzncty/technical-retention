# Case 147 grounding — Amazon S3 multipart upload pre-object retention (2010–2016, maintained contract)

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
